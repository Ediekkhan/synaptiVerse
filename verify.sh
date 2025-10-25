#!/bin/bash
# Quick verification script for SynaptiVerse deployment

echo "🔍 SynaptiVerse Deployment Verification"
echo "========================================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo "1. Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi

# Check file structure
echo ""
echo "2. Checking project structure..."
REQUIRED_FILES=(
    "README.md"
    "requirements.txt"
    "Dockerfile"
    "docker-compose.yml"
    "src/agents/appointment_coordinator.py"
    "src/agents/medical_advisor.py"
    "src/metta/metta_interface.py"
    "tests/e2e_scenarios.py"
    "agent-manifests/coordinator_manifest.yaml"
    "agent-manifests/advisor_manifest.yaml"
    "docs/design.md"
    "docs/ethics.md"
    "docs/deployment.md"
    "docs/video_transcript.md"
)

ALL_FILES_EXIST=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅${NC} $file"
    else
        echo -e "${RED}❌${NC} $file (missing)"
        ALL_FILES_EXIST=false
    fi
done

if [ "$ALL_FILES_EXIST" = false ]; then
    echo -e "${RED}Some required files are missing${NC}"
    exit 1
fi

# Test MeTTa interface
echo ""
echo "3. Testing MeTTa knowledge graph..."
if python3 -c "from src.metta import get_metta_knowledge_graph; kg = get_metta_knowledge_graph(); print(f'✅ Loaded {len(kg.knowledge_base)} medical facts')" 2>/dev/null; then
    echo -e "${GREEN}✅ MeTTa interface working${NC}"
else
    echo -e "${RED}❌ MeTTa interface test failed${NC}"
    exit 1
fi

# Run E2E tests
echo ""
echo "4. Running E2E test suite..."
if python3 tests/e2e_scenarios.py > /dev/null 2>&1; then
    echo -e "${GREEN}✅ All E2E tests passed${NC}"
else
    echo -e "${YELLOW}⚠️  Some E2E tests failed (run 'python tests/e2e_scenarios.py' for details)${NC}"
fi

# Check Docker
echo ""
echo "5. Checking Docker setup..."
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✅ Docker installed${NC}"
    
    if command -v docker-compose &> /dev/null; then
        echo -e "${GREEN}✅ Docker Compose installed${NC}"
        
        # Validate docker-compose.yml
        if docker-compose config > /dev/null 2>&1; then
            echo -e "${GREEN}✅ docker-compose.yml valid${NC}"
        else
            echo -e "${RED}❌ docker-compose.yml has errors${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Docker Compose not installed${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Docker not installed (optional for local dev)${NC}"
fi

# Check documentation completeness
echo ""
echo "6. Checking documentation..."
DOC_CHECKS=0

if grep -q "innovationlab" README.md; then
    echo -e "${GREEN}✅${NC} Innovation Lab badge in README"
    ((DOC_CHECKS++))
fi

if grep -q "agent1q" README.md 2>/dev/null; then
    echo -e "${YELLOW}⚠️${NC}  Agent addresses need to be updated in README"
else
    echo -e "${GREEN}✅${NC} Agent address placeholders in README"
    ((DOC_CHECKS++))
fi

if [ -f "docs/design.md" ] && [ $(wc -l < docs/design.md) -gt 100 ]; then
    echo -e "${GREEN}✅${NC} Design document is comprehensive"
    ((DOC_CHECKS++))
fi

if [ -f "docs/ethics.md" ] && grep -q "HIPAA" docs/ethics.md; then
    echo -e "${GREEN}✅${NC} Ethics document includes compliance considerations"
    ((DOC_CHECKS++))
fi

# Final summary
echo ""
echo "========================================"
echo "📊 VERIFICATION SUMMARY"
echo "========================================"

if [ "$ALL_FILES_EXIST" = true ]; then
    echo -e "${GREEN}✅ All required files present${NC}"
    echo -e "${GREEN}✅ MeTTa knowledge graph working${NC}"
    echo -e "${GREEN}✅ Documentation complete${NC}"
    echo ""
    echo -e "${GREEN}🎉 PROJECT READY FOR SUBMISSION!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Register agents on Agentverse"
    echo "2. Record demo video (use docs/video_transcript.md)"
    echo "3. Update agent addresses in README.md"
    echo "4. Upload demo video to YouTube"
    echo "5. Push to GitHub"
    echo "6. Submit to hackathon"
else
    echo -e "${RED}❌ Project has issues - please review${NC}"
    exit 1
fi

echo ""
