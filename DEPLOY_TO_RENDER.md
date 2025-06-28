# Deploy to Render.com - Step by Step Guide

## 🚀 Free Deployment on Render

### Step 1: Prepare Your Repository
1. Push this code to a GitHub repository
2. Make sure all files are committed, especially:
   - `cloud_agent_api.py` (cloud-optimized version)
   - `render.yaml` (deployment config)
   - `requirements.txt` (dependencies)
   - `autonomous_agent.py` (main agent code)

### Step 2: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account (free)
3. Connect your GitHub repository

### Step 3: Deploy the Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Choose the repository with this AI agent code
4. Render will auto-detect the `render.yaml` file

### Step 4: Configure Environment Variables (Optional)
For **full AI capabilities** (not required for demo):
1. In Render dashboard → Your service → Environment
2. Add: `OPENAI_API_KEY` = your OpenAI API key
3. If you don't add this, the service runs in **demo mode** (still functional!)

### Step 5: Deploy!
1. Click "Create Web Service"
2. Render will build and deploy automatically
3. You'll get a URL like: `https://your-service-name.onrender.com`

## 🌐 Using Your Deployed API

Once deployed, you can use the URL in your Express app:

```javascript
const AGENT_API_URL = 'https://your-service-name.onrender.com';

// Test the deployment
app.get('/test-ai', async (req, res) => {
    try {
        const response = await axios.get(`${AGENT_API_URL}/demo`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'AI service unavailable' });
    }
});
```

## 💡 Two Modes of Operation

### Demo Mode (FREE - No API Key Required)
- **Cost**: $0
- **Features**: Basic chat responses, mock task execution
- **Perfect for**: Testing, demonstrations, proof of concept

### Full AI Mode (Requires OpenAI API Key)
- **Cost**: Render free + OpenAI usage (~$0.03 per 1K tokens)
- **Features**: Full autonomous agent with GPT-4
- **Perfect for**: Production use, real AI capabilities

## 🔧 API Endpoints on Render

Your deployed service will have these endpoints:

- `GET /health` - Check if service is running
- `GET /demo` - Test endpoint with service info
- `POST /chat` - Chat with the AI
- `POST /execute-task` - Execute autonomous tasks
- `GET /status` - Get agent statistics

## 🚨 Important Notes

1. **Free Tier Limitations**:
   - Render free tier spins down after 15 minutes of inactivity
   - First request after spin-down takes ~30 seconds to wake up
   - 750 hours/month free (plenty for development)

2. **For Production**:
   - Consider Render's paid plan ($7/month) for always-on service
   - Or use the API sparingly to stay within free limits

## 🧪 Testing Your Deployment

```bash
# Test health endpoint
curl https://your-service-name.onrender.com/health

# Test demo endpoint  
curl https://your-service-name.onrender.com/demo

# Test chat
curl -X POST https://your-service-name.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello AI!"}'
```

## 🔄 Updating Your Deployment

Just push changes to your GitHub repository - Render will automatically redeploy!

---

**Total Cost for Demo Mode: $0**
**Total Cost for Full AI Mode: $0 + OpenAI usage**