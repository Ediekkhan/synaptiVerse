# 🚀 SynaptiVerse Deployment Guide
## Get Your Live Link for Hackathon Submission

---

## ⚡ Quick Deploy (Recommended for Hackathon)

### **Option 1: Render.com** (Easiest - 5 minutes)

**Why Render**: 
- ✅ Free tier available
- ✅ One-click deploy from GitHub
- ✅ Auto-deployment on push
- ✅ HTTPS included
- ✅ No credit card required

#### **Step-by-Step Instructions**:

1. **Push to GitHub** (if not done):
   ```bash
   git init
   git add .
   git commit -m "Deploy SynaptiVerse"
   git remote add origin https://github.com/YOUR_USERNAME/synaptiVerse.git
   git push -u origin main
   ```

2. **Go to Render**:
   - Visit: https://render.com
   - Click "Get Started for Free"
   - Sign up with GitHub

3. **Deploy**:
   - Click "New +" → "Blueprint"
   - Connect your GitHub repo: `synaptiVerse`
   - Render will detect `render.yaml` automatically
   - Click "Apply"
   
4. **Wait 2-5 minutes** for deployment

5. **Get Your Live Link**:
   - Format: `https://synaptiverse.onrender.com`
   - Copy this link for hackathon submission!

**Your Live Link**: `https://synaptiverse.onrender.com`

---

### **Option 2: Railway.app** (Fast - 3 minutes)

**Why Railway**:
- ✅ Free $5/month credit
- ✅ GitHub integration
- ✅ Fast deployments
- ✅ Auto-scaling

#### **Step-by-Step Instructions**:

1. **Push to GitHub** (if needed)

2. **Go to Railway**:
   - Visit: https://railway.app
   - Click "Start a New Project"
   - Login with GitHub

3. **Deploy from GitHub**:
   - Click "Deploy from GitHub repo"
   - Select `synaptiVerse`
   - Railway auto-detects Python
   - Click "Deploy"

4. **Add Domain**:
   - Go to Settings → Networking
   - Click "Generate Domain"
   - You'll get: `synaptiverse.up.railway.app`

5. **Set Environment Variables**:
   - Settings → Variables
   - Add these:
     ```
     PORT=8000
     HOST=0.0.0.0
     ENVIRONMENT=production
     DEBUG=False
     STORE_PHI=False
     ```

**Your Live Link**: `https://synaptiverse.up.railway.app`

---

### **Option 3: Fly.io** (Production-Ready)

**Why Fly**:
- ✅ Global edge deployment
- ✅ Free tier (3 VMs)
- ✅ Fast worldwide access
- ✅ Great for production

#### **Step-by-Step Instructions**:

1. **Install Fly CLI**:
   ```bash
   # macOS
   brew install flyctl
   
   # Or via script
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**:
   ```bash
   flyctl auth login
   ```

3. **Deploy** (from project directory):
   ```bash
   cd /Users/mac/synaptiVerse
   flyctl launch --now
   ```
   
   - App name: `synaptiverse` (or auto-generated)
   - Region: Choose closest to you
   - PostgreSQL: No
   - Redis: No

4. **Get Your URL**:
   ```bash
   flyctl status
   ```
   
**Your Live Link**: `https://synaptiverse.fly.dev`

---

## 🔧 Troubleshooting

### **Deployment Failed**

#### **Missing Dependencies**:
Check `requirements.txt` includes all packages:
```bash
# Should see:
uagents
hyperon
fastapi
uvicorn
pydantic
```

#### **Port Issues**:
Ensure server uses environment PORT:
```python
# In web_ui.py (already done)
port = int(os.getenv("PORT", "8000"))
uvicorn.run(app, host="0.0.0.0", port=port)
```

#### **Build Timeout**:
- Render/Railway: Free tier can be slow
- Wait 5-10 minutes
- Check build logs

---

### **Site Not Loading**

#### **Check Deployment Status**:
- Render: Dashboard → Service → Logs
- Railway: Project → Deployments → Logs
- Fly: `flyctl logs`

#### **Health Check**:
Visit: `https://your-app.com/health`

Should return:
```json
{
  "status": "healthy",
  "service": "SynaptiVerse Healthcare API",
  "appointments": 0
}
```

---

### **MeTTa Knowledge Graph Not Loading**

Verify path in environment:
```bash
METTA_KNOWLEDGE_PATH=src/metta/knowledge_graphs/medical_facts.metta
```

If file missing, check:
```bash
# Ensure file exists in repo
ls src/metta/knowledge_graphs/
```

---

## 🎯 Hackathon Submission Checklist

Before submitting your live link:

### **Test Your Deployment**:
- [ ] Site loads at your URL
- [ ] Navbar shows "Agents Online"
- [ ] Can analyze symptoms:
  - Input: `fever headache body aches`
  - Expect: Results with appointment ID
- [ ] Emergency detection works:
  - Input: `chest pain shortness of breath`
  - Expect: CRITICAL red badge
- [ ] Timeline expands
- [ ] Dark mode toggles
- [ ] Mobile responsive (resize browser)

### **Get These Links**:
- [ ] **Live Demo URL**: `https://your-app.onrender.com`
- [ ] **GitHub Repo**: `https://github.com/YOUR_USERNAME/synaptiVerse`
- [ ] **Health Check**: `https://your-app.onrender.com/health`

---

## 📝 Add to Hackathon Form

### **Live Demo Link**:
```
https://synaptiverse.onrender.com
```

### **Project Description**:
```
SynaptiVerse - Autonomous Healthcare Coordination

Live demo featuring:
• Fetch.ai autonomous agents
• SingularityNET MeTTa reasoning (500+ medical facts)
• Real-time symptom analysis
• Emergency detection via multi-hop reasoning
• Privacy-first architecture (zero PHI storage)

Test the demo:
1. Click "Analyze Symptoms"
2. Enter: "fever headache body aches"
3. Watch MeTTa AI analyze and create appointment
4. Try emergency: "chest pain shortness of breath"
```

### **GitHub Repository**:
```
https://github.com/YOUR_USERNAME/synaptiVerse
```

---

## 🌐 Custom Domain (Optional)

### **Add Custom Domain to Render**:

1. **Buy Domain** (optional):
   - Namecheap, Google Domains, etc.
   - Example: `synaptiverse.ai`

2. **Add to Render**:
   - Dashboard → Service → Settings
   - Custom Domain → Add
   - Enter: `synaptiverse.ai`

3. **Update DNS**:
   - Add CNAME record:
     ```
     CNAME: www → synaptiverse.onrender.com
     ```

4. **Wait for SSL** (auto-provisioned)

---

## 💡 Pro Tips

### **Free Tier Limitations**:

**Render Free**:
- ✅ Sleeps after 15 min inactivity
- ✅ 750 hours/month
- ⚠️ First request after sleep takes 30s

**Solution for Demo**:
- Visit your link before judges test
- Keep tab open to prevent sleep
- Or: Ping service every 10 minutes

**Railway Free**:
- ✅ $5 credit/month
- ✅ No sleep
- ⚠️ Credit runs out if over-used

**Fly Free**:
- ✅ 3 VMs always on
- ✅ No sleep
- ✅ Best for 24/7 uptime

### **Improve Load Time**:

1. **Cache MeTTa Facts**:
   Already enabled in `.env`:
   ```bash
   METTA_CACHE_ENABLED=True
   ```

2. **Use CDN for Fonts**:
   Already using Google Fonts CDN

3. **Pre-warm** before demo:
   Visit site 2 minutes before showing judges

---

## 🚀 Deployment Status Check

### **Quick Health Check**:
```bash
curl https://your-app.onrender.com/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "service": "SynaptiVerse Healthcare API",
  "appointments": 0
}
```

### **Full Test**:
```bash
# Test symptom analysis
curl -X POST https://your-app.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "fever headache"}'
```

---

## 📊 Monitoring (Optional)

### **View Logs**:

**Render**:
```
Dashboard → Service → Logs (live tail)
```

**Railway**:
```
Project → Deployments → View Logs
```

**Fly**:
```bash
flyctl logs -a synaptiverse
```

### **Check Metrics**:
- Response time
- Memory usage
- Active connections

---

## 🎬 Update Demo Video

If you already recorded demo with localhost:

### **Option A**: Quick caption
Add text overlay:
```
"Now deployed at: https://synaptiverse.onrender.com"
```

### **Option B**: Record new ending
30-second clip showing:
1. Live URL in browser
2. Same demo flow
3. "Deployed on Render for ASI Alliance Hackathon"

---

## ✅ Final Checklist

Before submitting:

- [ ] **Pushed to GitHub**: All code committed
- [ ] **Deployed successfully**: Site loads
- [ ] **Health check passes**: `/health` returns 200
- [ ] **Tested symptom analysis**: Creates appointments
- [ ] **Tested emergency detection**: Shows CRITICAL
- [ ] **Mobile works**: Responsive on phone
- [ ] **Dark mode works**: Toggle button functional
- [ ] **Live link copied**: Added to hackathon form
- [ ] **GitHub link copied**: Added to hackathon form
- [ ] **README updated**: Includes live demo link

---

## 🎯 Recommended: Render.com

**For Hackathon Submission, use Render because**:
1. ✅ Fastest setup (5 minutes)
2. ✅ Free tier sufficient
3. ✅ Auto-SSL (HTTPS)
4. ✅ Good uptime for demos
5. ✅ No credit card needed

**Your deployment steps**:
```bash
# 1. Push to GitHub
git init
git add .
git commit -m "SynaptiVerse - ASI Alliance Hackathon"
git remote add origin https://github.com/YOUR_USERNAME/synaptiVerse.git
git push -u origin main

# 2. Go to Render.com
# 3. New Blueprint → Connect GitHub → Deploy
# 4. Get link: https://synaptiverse.onrender.com
# 5. Test and submit!
```

---

**Need Help?** Check logs or DM me the error message!

**Time to Deploy**: 5-10 minutes total

**Let's get your live link! 🚀**
