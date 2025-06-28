// Express.js integration with deployed AI Agent on Render
// Updated to work with cloud deployment

const express = require('express');
const axios = require('axios');
const app = express();

app.use(express.json());

// Configuration - UPDATE THIS WITH YOUR RENDER URL
const AGENT_API_URL = process.env.AI_AGENT_URL || 'https://your-service-name.onrender.com';

// Middleware to check if agent is ready (with cloud-friendly timeout)
async function checkAgentHealth(req, res, next) {
    try {
        const response = await axios.get(`${AGENT_API_URL}/health`, { 
            timeout: 30000 // 30 second timeout for cold starts
        });
        if (!response.data.agent_ready) {
            return res.status(503).json({ error: 'AI Agent not ready' });
        }
        next();
    } catch (error) {
        return res.status(503).json({ 
            error: 'AI Agent service unavailable',
            hint: 'Service may be spinning up (takes ~30s on first request)'
        });
    }
}

// Test endpoint to verify deployment
app.get('/api/test-ai', async (req, res) => {
    try {
        const response = await axios.get(`${AGENT_API_URL}/demo`, {
            timeout: 30000
        });
        res.json({
            success: true,
            deployment_status: 'AI Agent is deployed and accessible',
            ...response.data
        });
    } catch (error) {
        res.status(500).json({ 
            success: false,
            error: 'Could not reach AI Agent service',
            agent_url: AGENT_API_URL,
            hint: 'Check if the Render service is deployed correctly'
        });
    }
});

// Chat endpoint - for general conversations
app.post('/api/chat', checkAgentHealth, async (req, res) => {
    try {
        const { message } = req.body;
        
        if (!message) {
            return res.status(400).json({ error: 'Message is required' });
        }

        const response = await axios.post(`${AGENT_API_URL}/chat`, {
            message: message
        }, { timeout: 30000 });

        res.json({
            success: true,
            response: response.data.response,
            agent_type: response.data.agent_type,
            timestamp: response.data.timestamp
        });
    } catch (error) {
        console.error('Chat error:', error.message);
        res.status(500).json({ 
            success: false, 
            error: 'Failed to process chat request',
            details: error.response?.data || error.message
        });
    }
});

// Task execution endpoint - for autonomous tasks
app.post('/api/execute-task', checkAgentHealth, async (req, res) => {
    try {
        const { task, priority = 5 } = req.body;
        
        if (!task) {
            return res.status(400).json({ error: 'Task description is required' });
        }

        const response = await axios.post(`${AGENT_API_URL}/execute-task`, {
            task: task,
            priority: priority
        }, { timeout: 60000 }); // Longer timeout for task execution

        res.json({
            success: true,
            ...response.data
        });
    } catch (error) {
        console.error('Task execution error:', error.message);
        res.status(500).json({ 
            success: false, 
            error: 'Failed to execute task',
            details: error.response?.data || error.message
        });
    }
});

// Agent status endpoint
app.get('/api/agent/status', checkAgentHealth, async (req, res) => {
    try {
        const response = await axios.get(`${AGENT_API_URL}/status`, {
            timeout: 15000
        });
        res.json({
            success: true,
            deployed_url: AGENT_API_URL,
            ...response.data
        });
    } catch (error) {
        console.error('Status error:', error.message);
        res.status(500).json({ 
            success: false, 
            error: 'Failed to get agent status'
        });
    }
});

// E-commerce specific endpoints using the deployed AI
app.post('/api/ai-assistant/product-research', checkAgentHealth, async (req, res) => {
    try {
        const { productCategory, requirements } = req.body;
        
        const task = `Research ${productCategory} products that meet these requirements: ${requirements}. 
                     Provide a detailed analysis with recommendations, pricing insights, and market trends.`;
        
        const response = await axios.post(`${AGENT_API_URL}/execute-task`, {
            task: task,
            priority: 7
        }, { timeout: 60000 });
        
        res.json({
            success: true,
            research: response.data,
            source: 'AI Agent deployed on Render'
        });
    } catch (error) {
        res.status(500).json({ 
            success: false, 
            error: 'Failed to research products'
        });
    }
});

app.post('/api/ai-assistant/customer-support', checkAgentHealth, async (req, res) => {
    try {
        const { customerQuery, orderDetails } = req.body;
        
        const message = `Customer support query: ${customerQuery}
                        Order details: ${JSON.stringify(orderDetails)}
                        Please provide helpful assistance and next steps.`;
        
        const response = await axios.post(`${AGENT_API_URL}/chat`, {
            message: message
        }, { timeout: 30000 });
        
        res.json({
            success: true,
            supportResponse: response.data.response,
            agent_type: response.data.agent_type
        });
    } catch (error) {
        res.status(500).json({ 
            success: false, 
            error: 'Failed to process support request'
        });
    }
});

// Health check for your Express app
app.get('/health', (req, res) => {
    res.json({
        status: 'Express server healthy',
        ai_agent_url: AGENT_API_URL,
        timestamp: new Date().toISOString()
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Express server running on port ${PORT}`);
    console.log(`AI Agent URL: ${AGENT_API_URL}`);
    console.log('Test the integration at: http://localhost:3000/api/test-ai');
});

module.exports = app;