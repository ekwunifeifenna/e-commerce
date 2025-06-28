import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { FaRobot, FaBrain, FaCog } from "react-icons/fa";
import { v4 as uuidv4 } from "uuid";

const EnhancedChatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isVisible, setIsVisible] = useState(false);
  const [showLiveAgentOption, setShowLiveAgentOption] = useState(false);
  const [aiMode, setAiMode] = useState('dialogflow'); // 'dialogflow' or 'ai_agent'
  const [aiAgentAvailable, setAiAgentAvailable] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Generate or persist a session ID
  const [sessionId] = useState(() => {
    return localStorage.getItem("chatSessionId") || uuidv4();
  });

  useEffect(() => {
    localStorage.setItem("chatSessionId", sessionId);
  }, [sessionId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check AI Agent availability on mount
  useEffect(() => {
    checkAIAgentStatus();
  }, []);

  const checkAIAgentStatus = async () => {
    try {
      const response = await axios.get('/api/ai-agent/status');
      setAiAgentAvailable(response.data.available);
    } catch (error) {
      setAiAgentAvailable(false);
    }
  };

  // FAQ Data (keeping your existing FAQ)
  const faqData = {
    q1: "HarmonyKloud is a cloud-based practice management and clinical solution designed for ABA therapy providers. It streamlines administrative tasks, enhances clinical workflows, and integrates billing solutions to optimize practice efficiency.",
    q2: "HarmonyKloud is designed for ABA providers including BCBAs, RBTs, clinic administrators, and practice owners, as well as behavioral health providers looking for an all-in-one solution.",
    q3: "HarmonyKloud offers a seamless user experience with advanced features like automated billing, EVV integration, real-time reporting, and compliance tracking. It is built for scalability and interoperability.",
    // ... rest of your FAQ items
    q20: "To cancel your subscription, please contact our support team. We offer flexible plans and are happy to discuss any concerns."
  };

  // Function to handle FAQ selection
  const handleFAQSelect = (e) => {
    const key = e.target.value;
    if (key) {
      const selectedIndex = e.target.selectedIndex;
      const questionText = e.target.options[selectedIndex].text;
      const answer = faqData[key];
      
      setMessages((prev) => [
        ...prev,
        { role: "user", content: questionText },
        { role: "bot", content: answer, source: "faq" }
      ]);
      
      e.target.selectedIndex = 0;
    }
  };

  // Enhanced chat function that can use either Dialogflow or AI Agent
  const sendMessage = async (message = input) => {
    if (!message.trim()) return;
  
    const userMessage = { role: "user", content: message };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
  
    try {
      // Use enhanced chatbot endpoint that supports both modes
      const response = await axios.post('/api/chatbot-enhanced', {
        session_id: sessionId,
        message: message,
        useAIAgent: aiMode === 'ai_agent'
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
  
      const botMessage = {
        role: "bot",
        content: response.data.text,
        buttons: response.data.buttons || [],
        showOptions: response.data.showOptions || false,
        source: response.data.source || 'unknown',
        agent_type: response.data.agent_type
      };
  
      setMessages((prev) => [...prev, botMessage]);
      setShowLiveAgentOption(true);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { 
          role: "bot", 
          content: "Sorry, I'm having trouble connecting. Please try again later.",
          source: "error"
        },
      ]);
    }
  };

  // AI Agent specific task execution
  const executeAITask = async (taskDescription) => {
    if (!aiAgentAvailable) {
      setMessages((prev) => [
        ...prev,
        { 
          role: "bot", 
          content: "AI Agent is not available. Please use regular chat mode.",
          source: "error"
        }
      ]);
      return;
    }

    const userMessage = { role: "user", content: `Execute task: ${taskDescription}` };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await axios.post('/api/ai-agent/execute-task', {
        task: taskDescription,
        priority: 7
      });

      const botMessage = {
        role: "bot",
        content: response.data.result,
        source: "ai_agent_task",
        task_id: response.data.task_id,
        status: response.data.status
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { 
          role: "bot", 
          content: "Failed to execute AI task. Please try again.",
          source: "error"
        }
      ]);
    }
  };

  // ABA-specific AI support
  const getABASupport = async (query) => {
    if (!aiAgentAvailable) return;

    const userMessage = { role: "user", content: `ABA Support: ${query}` };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await axios.post('/api/ai-agent/aba-support', {
        query: query,
        context: "HarmonyKloud ABA therapy platform"
      });

      const botMessage = {
        role: "bot",
        content: response.data.response,
        source: "aba_support",
        specialized_support: response.data.specialized_support
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { 
          role: "bot", 
          content: "ABA support is temporarily unavailable.",
          source: "error"
        }
      ]);
    }
  };

  const handleLiveAgentRequest = () => {
    setMessages((prev) => [
      ...prev,
      { role: "bot", content: "Connecting you to a live agent... Please wait.", source: "system" },
    ]);
    window.location.href =
      "mailto:sales@harmonykloud.com?subject=Live%20Agent%20Inquiry";
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const getSourceIcon = (source) => {
    switch (source) {
      case 'ai_agent':
      case 'ai_agent_task':
        return <FaBrain className="inline mr-1" />;
      case 'dialogflow':
        return <FaRobot className="inline mr-1" />;
      case 'aba_support':
        return <FaCog className="inline mr-1" />;
      default:
        return <FaRobot className="inline mr-1" />;
    }
  };

  return (
    <div>
      {/* Chatbot Toggle Button */}
      <button
        onClick={() => setIsVisible(!isVisible)}
        className="fixed bottom-4 right-4 bg-green-600 text-white p-4 rounded-full shadow-lg hover:bg-green-700 transition-colors z-50"
      >
        <FaRobot size={24} />
      </button>

      {/* Chatbot Interface */}
      {isVisible && (
        <div className="fixed bottom-16 right-4 w-[500px] h-[700px] border rounded-lg shadow-lg flex flex-col bg-white z-50">
          <div className="bg-green-600 text-white p-4 text-center text-lg font-semibold rounded-t-lg">
            <div>Harmony Kloud Assistant</div>
            <div className="text-sm mt-1">
              Mode: {aiMode === 'ai_agent' ? 'AI Agent' : 'Dialogflow'}
              {aiAgentAvailable && (
                <span className="ml-2 text-green-200">● AI Available</span>
              )}
            </div>
          </div>

          {/* AI Mode Selector */}
          {aiAgentAvailable && (
            <div className="p-2 bg-gray-100 border-b">
              <div className="flex gap-2">
                <button
                  onClick={() => setAiMode('dialogflow')}
                  className={`px-3 py-1 rounded text-sm ${
                    aiMode === 'dialogflow' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-200 text-gray-700'
                  }`}
                >
                  <FaRobot className="inline mr-1" /> FAQ Mode
                </button>
                <button
                  onClick={() => setAiMode('ai_agent')}
                  className={`px-3 py-1 rounded text-sm ${
                    aiMode === 'ai_agent' 
                      ? 'bg-purple-600 text-white' 
                      : 'bg-gray-200 text-gray-700'
                  }`}
                >
                  <FaBrain className="inline mr-1" /> AI Mode
                </button>
              </div>
            </div>
          )}

          {/* FAQ Dropdown */}
          <div className="p-4 border-b">
            <h2 className="text-lg font-semibold mb-2">Quick Help</h2>
            <select
              onChange={handleFAQSelect}
              className="w-full p-2 border rounded mb-2"
            >
              <option value="">Select a question...</option>
              <option value="q1">What is HarmonyKloud?</option>
              <option value="q2">Who can use HarmonyKloud?</option>
              <option value="q3">What makes HarmonyKloud different?</option>
              <option value="q20">How can I cancel my subscription?</option>
            </select>
            
            {/* AI Agent specific options */}
            {aiMode === 'ai_agent' && aiAgentAvailable && (
              <div className="flex gap-2 mt-2">
                <button
                  onClick={() => getABASupport("Best practices for ABA therapy documentation")}
                  className="text-xs bg-purple-600 text-white px-2 py-1 rounded hover:bg-purple-700"
                >
                  ABA Best Practices
                </button>
                <button
                  onClick={() => executeAITask("Analyze current ABA therapy billing trends and compliance requirements")}
                  className="text-xs bg-indigo-600 text-white px-2 py-1 rounded hover:bg-indigo-700"
                >
                  Billing Analysis
                </button>
              </div>
            )}
            
            <button
              onClick={handleLiveAgentRequest}
              className="mt-2 w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
            >
              Speak to a Live Agent
            </button>
          </div>

          {/* Chat Message Area */}
          <div className="flex-1 p-4 overflow-y-auto bg-gray-50">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`mb-4 flex ${
                  msg.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[80%] p-3 rounded-lg ${
                    msg.role === "user"
                      ? "bg-green-600 text-white"
                      : "bg-gray-200 text-gray-900"
                  }`}
                >
                  <div className="text-xs opacity-75 mb-1 flex items-center">
                    {msg.role === "user" ? "You" : (
                      <>
                        {getSourceIcon(msg.source)}
                        {msg.source === 'ai_agent' && 'AI Agent'}
                        {msg.source === 'dialogflow' && 'Dialogflow'}
                        {msg.source === 'aba_support' && 'ABA Specialist'}
                        {msg.source === 'faq' && 'FAQ'}
                        {!msg.source && 'Assistant'}
                      </>
                    )}
                  </div>
                  <div className="whitespace-pre-wrap">{msg.content}</div>
                  {msg.buttons?.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-2">
                      {msg.buttons.map((btn, i) => (
                        <button
                          key={i}
                          onClick={() => sendMessage(btn.query)}
                          className="text-xs bg-white bg-opacity-20 px-2 py-1 rounded hover:bg-opacity-30"
                        >
                          {btn.text}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-4 border-t">
            <div className="flex gap-2">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder={
                  aiMode === 'ai_agent' 
                    ? "Ask for analysis, tasks, or ABA guidance..." 
                    : "Type your message..."
                }
                rows="1"
                className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 resize-none"
              />
              <button
                onClick={() => sendMessage()}
                className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors self-end"
              >
                Send
              </button>
            </div>
            <div className="text-xs text-gray-500 mt-1">
              Press Enter to send • {aiMode === 'ai_agent' && aiAgentAvailable ? 'AI Agent Mode' : 'FAQ Mode'}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EnhancedChatbot;