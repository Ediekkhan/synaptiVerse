# 🤖 Agentverse Registration Guide

## ✅ Your Agent Addresses

### **Appointment Coordinator Agent**:
```
agent1q22ehv9v3wgjgvnw72s52xjku2he3j5h3x7e9hreztkuef5v9esjv7fyyur
```

### **Medical Advisor Agent**:
```
agent1qv5kl3fpn8mn8gpju4m5n9uk6nshwd9uf4tpx7ncuuleg4x6syxw6g8t9xr
```

---

## 📋 Step-by-Step Agentverse Registration

### **Step 1: Go to Agentverse**

Visit: https://agentverse.ai

- Sign up / Log in with your email or wallet

---

### **Step 2: Upload Coordinator Manifest**

1. Click **"My Agents"** → **"+ New Agent"**
2. Select **"Upload Manifest"**
3. Upload file: [agent-manifests/coordinator_manifest.yaml](file:///Users/mac/synaptiVerse/agent-manifests/coordinator_manifest.yaml)
4. **Agent Address**: Paste coordinator address:
   ```
   agent1q22ehv9v3wgjgvnw72s52xjku2he3j5h3x7e9hreztkuef5v9esjv7fyyur
   ```
5. **Tags**: Add `Innovation Lab`, `Healthcare`, `ASI Alliance`
6. **Enable Chat Protocol**: ✅ Check this box
7. Click **"Publish"**

---

### **Step 3: Upload Advisor Manifest**

1. Click **"+ New Agent"** again
2. Select **"Upload Manifest"**
3. Upload file: [agent-manifests/advisor_manifest.yaml](file:///Users/mac/synaptiVerse/agent-manifests/advisor_manifest.yaml)
4. **Agent Address**: Paste advisor address:
   ```
   agent1qv5kl3fpn8mn8gpju4m5n9uk6nshwd9uf4tpx7ncuuleg4x6syxw6g8t9xr
   ```
5. **Tags**: Add `Innovation Lab`, `Healthcare`, `MeTTa`, `Knowledge Graph`
6. **Enable Chat Protocol**: ✅ Check this box
7. Click **"Publish"**

---

## 📝 Update Your Documentation

### **1. Update README.md**

Add agent addresses to your GitHub README:

```markdown
## 🤖 Agent Addresses

### Testnet Agents:
- **Appointment Coordinator**: `agent1q22ehv9v3wgjgvnw72s52xjku2he3j5h3x7e9hreztkuef5v9esjv7fyyur`
- **Medical Advisor**: `agent1qv5kl3fpn8mn8gpju4m5n9uk6nshwd9uf4tpx7ncuuleg4x6syxw6g8t9xr`

### Agentverse:
- View on Agentverse: https://agentverse.ai/agents/agent1q22ehv9v3wgjgvnw72s52xjku2he3j5h3x7e9hreztkuef5v9esjv7fyyur
- Chat Protocol Enabled: ✅
```

---

### **2. Update Hackathon Submission**

Add to your submission form:

**Agent Addresses**:
```
Coordinator: agent1q22ehv9v3wgjgvnw72s52xjku2he3j5h3x7e9hreztkuef5v9esjv7fyyur
Advisor: agent1qv5kl3fpn8mn8gpju4m5n9uk6nshwd9uf4tpx7ncuuleg4x6syxw6g8t9xr
```

**Agentverse Links**:
```
https://agentverse.ai/agents/agent1q22ehv9v3wgjgvnw72s52xjku2he3j5h3x7e9hreztkuef5v9esjv7fyyur
https://agentverse.ai/agents/agent1qv5kl3fpn8mn8gpju4m5n9uk6nshwd9uf4tpx7ncuuleg4x6syxw6g8t9xr
```

---

## 🎯 What These Agents Do

### **Appointment Coordinator** (`agent1q22e...`):
- **Function**: Main entry point for patient requests
- **Capabilities**:
  - Receives appointment requests
  - Parses patient symptoms
  - Coordinates with Medical Advisor
  - Schedules appointments with appropriate specialists
- **Chat Protocol**: Can interact with users via Agentverse chat
- **Manifest**: [coordinator_manifest.yaml](file:///Users/mac/synaptiVerse/agent-manifests/coordinator_manifest.yaml)

### **Medical Advisor** (`agent1qv5k...`):
- **Function**: Medical knowledge analysis engine
- **Capabilities**:
  - Queries MeTTa knowledge graph (500+ medical facts)
  - Performs multi-hop reasoning
  - Provides differential diagnosis
  - Recommends appropriate specialists
  - Detects emergency conditions
- **Knowledge Base**: 8 clinical categories, 500+ facts
- **Manifest**: [advisor_manifest.yaml](file:///Users/mac/synaptiVerse/agent-manifests/advisor_manifest.yaml)

---

## 🔗 Integration Points

### **How They Work Together**:
```
User Request 
   → Appointment Coordinator (agent1q22e...)
   → Medical Advisor (agent1qv5k...)
   → MeTTa Knowledge Graph
   → Response with Specialist & Urgency
   → Appointment Scheduled
```

### **Communication Protocol**:
- **Local**: Direct agent-to-agent messaging
- **Agentverse**: Chat Protocol enabled
- **Future**: Can discover other agents (insurance, pharmacy, labs)

---

## ✅ Verification Checklist

After uploading to Agentverse:

- [ ] **Coordinator agent** visible in "My Agents"
- [ ] **Advisor agent** visible in "My Agents"  
- [ ] Both agents show **"Active"** status
- [ ] **Chat Protocol** enabled on both
- [ ] **Tags** added (Innovation Lab, Healthcare, etc.)
- [ ] **Addresses** match the ones above
- [ ] Can send test message via Chat interface

---

## 🧪 Test Agentverse Chat

### **Test Message for Coordinator**:
```
I have fever, headache, and body aches. Need appointment tomorrow.
```

**Expected Response**:
```
Appointment created:
- Condition: Influenza (87% confidence)
- Specialist: Primary Care Physician  
- Urgency: Routine
- Appointment ID: APT-XXXXXXXX
```

---

## 📊 Hackathon Submission Checklist

For your ASI Alliance submission, include:

- [x] **Live Demo**: https://synaptiverse.onrender.com ✅
- [x] **GitHub Repo**: https://github.com/Ediekkhan/synaptiVerse ✅
- [ ] **Agent Addresses**: (copy from above)
- [ ] **Agentverse Links**: (after registration)
- [ ] **Manifests**: Both uploaded and published
- [ ] **Chat Protocol**: Enabled and tested
- [ ] **Video Demo**: (optional but recommended)

---

## 🎬 Demo Script Enhancement

Add to your demo:

**"Our agents are live on Agentverse!"**

1. Show Agentverse page with your agents
2. Send test message via Chat interface
3. Show real-time response
4. Highlight autonomous coordination

**Talking Points**:
- "Two autonomous agents working together"
- "Registered on Fetch.ai Agentverse"
- "Chat Protocol enabled for human interaction"
- "Can discover and integrate with other agents"

---

## 🚀 Next Steps After Registration

1. **Test agents** on Agentverse via Chat
2. **Update README** with addresses
3. **Add to submission** form
4. **Screenshot** Agentverse dashboard
5. **Include in presentation** slides
6. **Mention in Twitter** thread

---

## 📞 Need Help?

**Agentverse Issues**:
- Support: https://fetch.ai/docs/guides/agents/getting-started
- Discord: https://discord.gg/fetchai

**Agent Not Showing**:
- Verify address is correct
- Check manifest YAML syntax
- Ensure Chat Protocol compatible

---

## 🎉 You're Ready!

**Your Agents**:
✅ Coordinator: `agent1q22e...`  
✅ Advisor: `agent1qv5k...`

**Next**: Upload to Agentverse and complete your hackathon submission!

**Your complete submission**:
- ✅ Live web app: https://synaptiverse.onrender.com
- ✅ GitHub code: https://github.com/Ediekkhan/synaptiVerse
- 🔄 Agentverse agents: (upload now!)
- ✅ Documentation: Complete
- ✅ Tests: 9/9 passing

**You're 95% done - just register the agents!** 🚀
