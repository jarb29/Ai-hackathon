const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const { EventEmitter } = require('events');

// Configuration
const CONFIG = {
    port: parseInt(process.env.MCP_PORT) || 3001,
    mcpTimeout: parseInt(process.env.MCP_TIMEOUT) || 30000,
    initTimeout: parseInt(process.env.MCP_INIT_TIMEOUT) || 5000,
    protocolVersion: '2024-11-05',
    serviceName: 'chrome-mcp-http-service',
    serviceVersion: '1.0.0'
};

// Logger utility
class Logger {
    static info(message, ...args) {
        console.log(`[INFO] ${new Date().toISOString()} - ${message}`, ...args);
    }
    
    static error(message, ...args) {
        console.error(`[ERROR] ${new Date().toISOString()} - ${message}`, ...args);
    }
    
    static warn(message, ...args) {
        console.warn(`[WARN] ${new Date().toISOString()} - ${message}`, ...args);
    }
}

// MCP Service Manager
class MCPServiceManager extends EventEmitter {
    constructor() {
        super();
        this.process = null;
        this.isReady = false;
        this.requestId = 1;
        this.pendingRequests = new Map();
    }
    
    async start() {
        if (this.process) {
            Logger.warn('MCP process already running');
            return;
        }
        
        Logger.info('Starting MCP Chrome DevTools server');
        
        this.process = spawn('npx', [
            'chrome-devtools-mcp',
            '--headless=true',
            '--isolated=true'
        ], {
            stdio: ['pipe', 'pipe', 'pipe'],
            env: {
                ...process.env,
                CHROME_BIN: '/usr/bin/chromium',
                PUPPETEER_EXECUTABLE_PATH: '/usr/bin/chromium'
            }
        });
        
        this._setupProcessHandlers();
        
        // Initialize with timeout
        setTimeout(async () => {
            if (this.process && !this.process.killed) {
                try {
                    await this._initialize();
                    this.isReady = true;
                    Logger.info('MCP Chrome DevTools server ready');
                    this.emit('ready');
                } catch (error) {
                    Logger.error('MCP initialization failed:', error.message);
                    this.isReady = false;
                    this.emit('error', error);
                }
            }
        }, CONFIG.initTimeout);
    }
    
    _setupProcessHandlers() {
        this.process.stdout.on('data', (data) => {
            this._handleResponse(data);
        });
        
        this.process.stderr.on('data', (data) => {
            Logger.warn('MCP stderr:', data.toString().trim());
        });
        
        this.process.on('error', (error) => {
            Logger.error('MCP process error:', error.message);
            this.isReady = false;
            this.emit('error', error);
        });
        
        this.process.on('exit', (code) => {
            Logger.info(`MCP process exited with code: ${code}`);
            this.isReady = false;
            this.process = null;
            this._rejectPendingRequests(new Error('MCP process terminated'));
            this.emit('exit', code);
        });
    }
    
    _handleResponse(data) {
        try {
            const lines = data.toString().split('\n').filter(line => line.trim());
            for (const line of lines) {
                const response = JSON.parse(line);
                const pendingRequest = this.pendingRequests.get(response.id);
                
                if (pendingRequest) {
                    this.pendingRequests.delete(response.id);
                    clearTimeout(pendingRequest.timeout);
                    
                    if (response.error) {
                        pendingRequest.reject(new Error(`MCP error: ${JSON.stringify(response.error)}`));
                    } else {
                        pendingRequest.resolve(response.result);
                    }
                }
            }
        } catch (error) {
            Logger.warn('Failed to parse MCP response:', error.message);
        }
    }
    
    async _initialize() {
        const initRequest = {
            jsonrpc: '2.0',
            id: this.requestId++,
            method: 'initialize',
            params: {
                protocolVersion: CONFIG.protocolVersion,
                capabilities: {},
                clientInfo: {
                    name: CONFIG.serviceName,
                    version: CONFIG.serviceVersion
                }
            }
        };
        
        return this._sendRequest(initRequest);
    }
    
    async executeTool(toolName, args) {
        if (!this.isReady || !this.process || this.process.killed) {
            throw new Error('MCP server not ready');
        }
        
        const toolRequest = {
            jsonrpc: '2.0',
            id: this.requestId++,
            method: 'tools/call',
            params: {
                name: toolName,
                arguments: args
            }
        };
        
        return this._sendRequest(toolRequest);
    }
    
    _sendRequest(request) {
        return new Promise((resolve, reject) => {
            if (!this.process || this.process.killed) {
                reject(new Error('MCP process not available'));
                return;
            }
            
            const timeout = setTimeout(() => {
                this.pendingRequests.delete(request.id);
                reject(new Error(`MCP request timeout after ${CONFIG.mcpTimeout}ms`));
            }, CONFIG.mcpTimeout);
            
            this.pendingRequests.set(request.id, { resolve, reject, timeout });
            
            const requestStr = JSON.stringify(request) + '\n';
            this.process.stdin.write(requestStr);
        });
    }
    
    _rejectPendingRequests(error) {
        for (const [id, request] of this.pendingRequests) {
            clearTimeout(request.timeout);
            request.reject(error);
        }
        this.pendingRequests.clear();
    }
    
    async stop() {
        if (this.process) {
            Logger.info('Stopping MCP server');
            this.process.kill('SIGTERM');
            this.process = null;
            this.isReady = false;
        }
    }
    
    getStatus() {
        return {
            ready: this.isReady,
            processAlive: this.process && !this.process.killed,
            pendingRequests: this.pendingRequests.size
        };
    }
}

// Tool definitions
const TOOL_DEFINITIONS = [
    {
        name: "navigate_page",
        description: "Navigate to a webpage and capture basic metrics",
        inputSchema: {
            type: "object",
            properties: {
                url: { type: "string", description: "URL to navigate to" }
            },
            required: ["url"]
        }
    },
    {
        name: "performance_start_trace",
        description: "Start performance tracing for Core Web Vitals",
        inputSchema: {
            type: "object",
            properties: {
                reload: { type: "boolean", description: "Whether to reload the page" }
            }
        }
    },
    {
        name: "performance_stop_trace",
        description: "Stop performance tracing and get results",
        inputSchema: {
            type: "object",
            properties: {}
        }
    },
    {
        name: "evaluate_script",
        description: "Execute JavaScript in the page context",
        inputSchema: {
            type: "object",
            properties: {
                script: { type: "string", description: "JavaScript code to execute" }
            }
        }
    },
    {
        name: "take_screenshot",
        description: "Take a screenshot of the current page",
        inputSchema: {
            type: "object",
            properties: {
                fullPage: { type: "boolean", description: "Capture full page" }
            }
        }
    },
    {
        name: "list_network_requests",
        description: "Get network requests made by the page",
        inputSchema: {
            type: "object",
            properties: {}
        }
    }
];

// Initialize service manager
const mcpManager = new MCPServiceManager();

// Express app setup
const app = express();

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// Request logging middleware
app.use((req, res, next) => {
    Logger.info(`${req.method} ${req.path}`);
    next();
});

// Health check endpoint
app.get('/health', (req, res) => {
    const status = mcpManager.getStatus();
    const isHealthy = status.ready && status.processAlive;
    
    res.status(isHealthy ? 200 : 503).json({
        status: isHealthy ? 'healthy' : 'unhealthy',
        service: CONFIG.serviceName,
        version: CONFIG.serviceVersion,
        uptime: process.uptime(),
        timestamp: new Date().toISOString(),
        mcp: status
    });
});

// MCP tools list endpoint
app.get('/mcp/tools', (req, res) => {
    if (!mcpManager.getStatus().ready) {
        return res.status(503).json({
            error: 'MCP server not ready',
            status: mcpManager.getStatus()
        });
    }
    
    res.json({ 
        tools: TOOL_DEFINITIONS,
        count: TOOL_DEFINITIONS.length,
        timestamp: new Date().toISOString()
    });
});

// MCP tool execution endpoint
app.post('/mcp/tools/:toolName', async (req, res) => {
    const startTime = Date.now();
    const { toolName } = req.params;
    const { arguments: toolArgs = {} } = req.body;
    
    // Validate tool exists
    const toolExists = TOOL_DEFINITIONS.some(tool => tool.name === toolName);
    if (!toolExists) {
        return res.status(400).json({
            success: false,
            error: `Unknown tool: ${toolName}`,
            availableTools: TOOL_DEFINITIONS.map(t => t.name)
        });
    }
    
    // Check MCP readiness
    if (!mcpManager.getStatus().ready) {
        return res.status(503).json({
            success: false,
            error: 'MCP server not ready',
            status: mcpManager.getStatus()
        });
    }
    
    try {
        Logger.info(`Executing tool: ${toolName}`, toolArgs);
        
        const result = await mcpManager.executeTool(toolName, toolArgs);
        const duration = Date.now() - startTime;
        
        Logger.info(`Tool ${toolName} completed in ${duration}ms`);
        
        res.json({
            success: true,
            result,
            metadata: {
                tool: toolName,
                duration,
                timestamp: new Date().toISOString()
            }
        });
    } catch (error) {
        const duration = Date.now() - startTime;
        Logger.error(`Tool ${toolName} failed after ${duration}ms:`, error.message);
        
        res.status(500).json({
            success: false,
            error: error.message,
            metadata: {
                tool: toolName,
                duration,
                timestamp: new Date().toISOString()
            }
        });
    }
});

// Error handling middleware
app.use((error, req, res, next) => {
    Logger.error('Unhandled error:', error.message);
    res.status(500).json({
        success: false,
        error: 'Internal server error',
        timestamp: new Date().toISOString()
    });
});

// 404 handler
app.use('*', (req, res) => {
    res.status(404).json({
        success: false,
        error: 'Endpoint not found',
        availableEndpoints: ['/health', '/mcp/tools', '/mcp/tools/:toolName'],
        timestamp: new Date().toISOString()
    });
});

// Graceful shutdown handler
const gracefulShutdown = async (signal) => {
    Logger.info(`Received ${signal}, shutting down gracefully`);
    
    try {
        await mcpManager.stop();
        Logger.info('MCP service stopped');
        process.exit(0);
    } catch (error) {
        Logger.error('Error during shutdown:', error.message);
        process.exit(1);
    }
};

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

// Unhandled rejection handler
process.on('unhandledRejection', (reason, promise) => {
    Logger.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

// Start server
const server = app.listen(CONFIG.port, async () => {
    Logger.info(`Chrome MCP Service listening on port ${CONFIG.port}`);
    Logger.info('Configuration:', CONFIG);
    
    try {
        await mcpManager.start();
        Logger.info('Service initialization completed');
    } catch (error) {
        Logger.error('Failed to start MCP service:', error.message);
        process.exit(1);
    }
});

// Handle server errors
server.on('error', (error) => {
    Logger.error('Server error:', error.message);
    process.exit(1);
});