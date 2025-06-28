// AI Agent Integration Routes
// Add these routes to your existing Express server

import axios from 'axios';

// Configuration - Update this with your deployed Render URL
const AI_AGENT_URL = process.env.AI_AGENT_URL || 'https://your-service-name.onrender.com';

// AI Agent middleware to check if service is available
const checkAIAgent = async (req, res, next) => {
  try {
    const response = await axios.get(`${AI_AGENT_URL}/health`, { timeout: 5000 });
    req.aiAgentAvailable = response.data.agent_ready;
    next();
  } catch (error) {
    req.aiAgentAvailable = false;
    next();
  }
};

// Enhanced chatbot route with AI Agent fallback
app.post("/api/chatbot-enhanced", checkAIAgent, async (req, res) => {
  try {
    const { message, sessionId = "default-session", useAIAgent = false } = req.body;

    if (!message) {
      return res.status(400).json({ error: "Message is required" });
    }

    // If AI Agent is requested and available, use it
    if (useAIAgent && req.aiAgentAvailable) {
      try {
        const aiResponse = await axios.post(`${AI_AGENT_URL}/chat`, {
          message: message
        }, { timeout: 10000 });

        return res.json({
          text: aiResponse.data.response,
          source: 'ai_agent',
          agent_type: aiResponse.data.agent_type,
          timestamp: aiResponse.data.timestamp,
          buttons: [],
          showOptions: false
        });
      } catch (aiError) {
        console.log("AI Agent failed, falling back to Dialogflow:", aiError.message);
      }
    }

    // Fallback to your existing Dialogflow logic
    const sessionPath = dialogflowClient.projectLocationAgentSessionPath(
      process.env.GOOGLE_PROJECT_ID,
      process.env.GOOGLE_AGENT_LOCATION,
      process.env.GOOGLE_AGENT_ID,
      sessionId
    );

    const request = {
      session: sessionPath,
      queryInput: {
        text: { text: message },
        languageCode: "en-US",
      },
    };

    const [response] = await dialogflowClient.detectIntent(request);
    const result = response.queryResult;

    const botResponse = {
      text: result.responseMessages[0].text.text[0],
      source: 'dialogflow',
      buttons: [],
      showOptions: false,
    };

    if (result.responseMessages[0].payload) {
      botResponse.buttons =
        result.responseMessages[0].payload.fields.buttons.listValue.values.map(
          (btn) => ({
            text: btn.structValue.fields.text.stringValue,
            query: btn.structValue.fields.query.stringValue,
          })
        );
    }

    if (
      botResponse.buttons.length === 0 &&
      result.intent?.displayName === "Default Fallback Intent"
    ) {
      botResponse.showOptions = true;
    }

    res.json(botResponse);
  } catch (error) {
    console.error("Enhanced Chatbot Error:", error);
    res.status(500).json({
      text: "Sorry, I'm having trouble connecting. Please try again later.",
      showOptions: true,
    });
  }
});

// AI Agent task execution route
app.post("/api/ai-agent/execute-task", checkAIAgent, async (req, res) => {
  try {
    if (!req.aiAgentAvailable) {
      return res.status(503).json({ 
        error: 'AI Agent service not available',
        fallback: 'Using basic response generation'
      });
    }

    const { task, priority = 5 } = req.body;
    
    if (!task) {
      return res.status(400).json({ error: 'Task description is required' });
    }

    const response = await axios.post(`${AI_AGENT_URL}/execute-task`, {
      task: task,
      priority: priority
    }, { timeout: 30000 });

    res.json({
      success: true,
      ...response.data
    });
  } catch (error) {
    console.error('AI Task execution error:', error.message);
    res.status(500).json({ 
      success: false, 
      error: 'Failed to execute AI task',
      details: error.response?.data || error.message
    });
  }
});

// E-commerce specific AI routes
app.post("/api/ai-agent/product-research", checkAIAgent, async (req, res) => {
  try {
    if (!req.aiAgentAvailable) {
      return res.status(503).json({ error: 'AI Agent service not available' });
    }

    const { productCategory, requirements } = req.body;
    
    const task = `Research ${productCategory} products that meet these requirements: ${requirements}. 
                 Provide detailed analysis with recommendations, pricing insights, and market trends.`;
    
    const response = await axios.post(`${AI_AGENT_URL}/execute-task`, {
      task: task,
      priority: 7
    }, { timeout: 60000 });
    
    res.json({
      success: true,
      research: response.data,
      source: 'AI Agent on Render.com'
    });
  } catch (error) {
    res.status(500).json({ 
      success: false, 
      error: 'Failed to research products'
    });
  }
});

// Healthcare/ABA specific AI assistant
app.post("/api/ai-agent/aba-support", checkAIAgent, async (req, res) => {
  try {
    if (!req.aiAgentAvailable) {
      return res.status(503).json({ error: 'AI Agent service not available' });
    }

    const { query, context } = req.body;
    
    const message = `ABA Therapy Support Query: ${query}
                    Context: ${context}
                    Please provide professional guidance for ABA therapy providers, including clinical recommendations, administrative support, and best practices.`;
    
    const response = await axios.post(`${AI_AGENT_URL}/chat`, {
      message: message
    }, { timeout: 30000 });
    
    res.json({
      success: true,
      response: response.data.response,
      agent_type: response.data.agent_type,
      specialized_support: 'ABA Therapy'
    });
  } catch (error) {
    res.status(500).json({ 
      success: false, 
      error: 'Failed to process ABA support request'
    });
  }
});

// AI Agent status check
app.get("/api/ai-agent/status", checkAIAgent, async (req, res) => {
  try {
    if (!req.aiAgentAvailable) {
      return res.json({
        available: false,
        message: 'AI Agent service is not available',
        fallback: 'Using Dialogflow for chat functionality'
      });
    }

    const response = await axios.get(`${AI_AGENT_URL}/status`, { timeout: 10000 });
    
    res.json({
      available: true,
      ai_agent_url: AI_AGENT_URL,
      ...response.data
    });
  } catch (error) {
    res.status(500).json({ 
      available: false,
      error: 'Failed to get AI agent status'
    });
  }
});

// Health check that includes AI Agent status
app.get("/api/health-extended", checkAIAgent, (req, res) => {
  res.json({
    server_status: 'healthy',
    dialogflow_available: true,
    ai_agent_available: req.aiAgentAvailable,
    ai_agent_url: AI_AGENT_URL,
    timestamp: new Date().toISOString()
  });
});