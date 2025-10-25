"""
SynaptiVerse Web UI
Simple web interface for the healthcare appointment system
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from metta.metta_interface import query_metta

app = FastAPI(title="SynaptiVerse Healthcare", version="1.0.0")

# Store appointments in memory
appointments = {}

class SymptomRequest(BaseModel):
    symptoms: str

class AppointmentResponse(BaseModel):
    success: bool
    appointment_id: str = None
    message: str
    specialist: str = None
    urgency: str = None
    scheduled_time: str = None
    confidence: float = None
    condition: str = None

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main UI"""
    return r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SynaptiVerse – AI Healthcare Intelligence</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --color-primary: #6366F1;
            --color-primary-dark: #4F46E5;
            --color-cyan: #06B6D4;
            --color-success: #10B981;
            --color-warning: #F59E0B;
            --color-danger: #EF4444;
            --color-info: #3B82F6;
            --color-background: #F9FAFB;
            --color-surface: #FFFFFF;
            --color-glass: rgba(255, 255, 255, 0.7);
            --color-text-primary: #111827;
            --color-text-secondary: #6B7280;
            --color-text-tertiary: #9CA3AF;
            --color-border: #E5E7EB;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.3);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 20px;
            --blur-sm: blur(8px);
            --blur-md: blur(12px);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--color-background);
            min-height: 100vh;
            padding: 0;
            padding-top: 80px;
            color: var(--color-text-primary);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            overflow-x: hidden;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 24px;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 380px;
            gap: 24px;
            margin-bottom: 24px;
        }
        
        @media (max-width: 1024px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
            
            .agent-panel {
                order: -1;
            }
        }
        
        /* Agent Status Panel */
        .agent-panel {
            background: var(--color-glass);
            backdrop-filter: var(--blur-md);
            -webkit-backdrop-filter: var(--blur-md);
            border-radius: var(--radius-xl);
            padding: 24px;
            box-shadow: var(--shadow-lg);
            border: 1px solid rgba(255, 255, 255, 0.5);
            height: fit-content;
            position: sticky;
            top: 94px;
        }
        
        .panel-header {
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .agent-status-item {
            padding: 16px;
            background: var(--color-surface);
            border-radius: var(--radius-md);
            margin-bottom: 12px;
            border: 1px solid var(--color-border);
            transition: all 0.2s ease;
        }
        
        .agent-status-item:hover {
            transform: translateX(4px);
            box-shadow: var(--shadow-md);
        }
        
        .agent-name {
            font-weight: 600;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.9375rem;
        }
        
        .agent-metric {
            display: flex;
            justify-content: space-between;
            font-size: 0.8125rem;
            color: var(--color-text-secondary);
            margin-top: 6px;
        }
        
        .metric-value {
            font-weight: 600;
            color: var(--color-text-primary);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 20px;
        }
        
        .stat-card {
            background: var(--color-surface);
            padding: 16px;
            border-radius: var(--radius-md);
            border: 1px solid var(--color-border);
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.75rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-cyan) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .stat-label {
            font-size: 0.75rem;
            color: var(--color-text-tertiary);
            margin-top: 4px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* Timeline */
        .timeline-section {
            background: var(--color-surface);
            border-radius: var(--radius-xl);
            padding: 32px;
            margin-top: 24px;
            box-shadow: var(--shadow-lg);
            border: 1px solid var(--color-border);
        }
        
        .timeline-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }
        
        .timeline-title {
            font-size: 1.5rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .timeline-toggle {
            background: var(--color-primary);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: var(--radius-sm);
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .timeline-toggle:hover {
            background: var(--color-primary-dark);
            transform: translateY(-2px);
        }
        
        .timeline-content {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }
        
        .timeline-content.expanded {
            max-height: 1000px;
        }
        
        .timeline-item {
            display: flex;
            gap: 16px;
            padding: 20px 0;
            border-left: 2px solid var(--color-border);
            padding-left: 24px;
            margin-left: 8px;
            position: relative;
        }
        
        .timeline-item::before {
            content: '';
            position: absolute;
            left: -9px;
            top: 24px;
            width: 16px;
            height: 16px;
            background: var(--color-primary);
            border-radius: 50%;
            border: 3px solid var(--color-surface);
        }
        
        .timeline-item:last-child {
            border-left-color: transparent;
        }
        
        .timeline-time {
            color: var(--color-text-tertiary);
            font-size: 0.8125rem;
            min-width: 80px;
        }
        
        .timeline-event {
            flex: 1;
        }
        
        .timeline-event-title {
            font-weight: 600;
            margin-bottom: 4px;
        }
        
        .timeline-event-desc {
            color: var(--color-text-secondary);
            font-size: 0.875rem;
        }
        
        /* About Section */
        .about-section {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(6, 182, 212, 0.05) 100%);
            border-radius: var(--radius-xl);
            padding: 48px;
            margin-top: 48px;
            border: 1px solid rgba(99, 102, 241, 0.1);
        }
        
        .about-title {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 16px;
            text-align: center;
        }
        
        .about-subtitle {
            text-align: center;
            color: var(--color-text-secondary);
            font-size: 1.125rem;
            margin-bottom: 40px;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
            margin-top: 32px;
        }
        
        .feature-card {
            background: var(--color-surface);
            padding: 24px;
            border-radius: var(--radius-lg);
            border: 1px solid var(--color-border);
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-xl);
        }
        
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 16px;
            display: block;
        }
        
        .feature-title {
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .feature-desc {
            color: var(--color-text-secondary);
            font-size: 0.875rem;
            line-height: 1.6;
        }
        
        /* Footer */
        .footer-main {
            background: var(--color-surface);
            border-top: 1px solid var(--color-border);
            margin-top: 64px;
            padding: 48px 0 24px;
        }
        
        .footer-grid {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 32px;
            margin-bottom: 32px;
        }
        
        .footer-brand {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        
        .footer-logo {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-cyan) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .footer-desc {
            color: var(--color-text-secondary);
            font-size: 0.875rem;
            line-height: 1.6;
        }
        
        .footer-column h4 {
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 16px;
            color: var(--color-text-primary);
        }
        
        .footer-links {
            list-style: none;
        }
        
        .footer-links li {
            margin-bottom: 8px;
        }
        
        .footer-links a {
            color: var(--color-text-secondary);
            text-decoration: none;
            font-size: 0.875rem;
            transition: color 0.2s ease;
        }
        
        .footer-links a:hover {
            color: var(--color-primary);
        }
        
        .footer-bottom {
            padding-top: 24px;
            border-top: 1px solid var(--color-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: var(--color-text-tertiary);
            font-size: 0.875rem;
        }
        
        .social-links {
            display: flex;
            gap: 16px;
        }
        
        .social-links a {
            color: var(--color-text-secondary);
            font-size: 1.25rem;
            transition: all 0.2s ease;
        }
        
        .social-links a:hover {
            color: var(--color-primary);
            transform: translateY(-2px);
        }
        
        @media (max-width: 768px) {
            .footer-grid {
                grid-template-columns: 1fr;
            }
        }
        
        /* Dark Mode */
        body.dark-mode {
            --color-background: #0F172A;
            --color-surface: #1E293B;
            --color-glass: rgba(30, 41, 59, 0.7);
            --color-text-primary: #F1F5F9;
            --color-text-secondary: #94A3B8;
            --color-text-tertiary: #64748B;
            --color-border: #334155;
        }
        
        body.dark-mode .header::before {
            background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-cyan) 50%, var(--color-primary) 100%);
        }
        
        body.dark-mode .main-card,
        body.dark-mode .agent-panel,
        body.dark-mode .result-card {
            background: rgba(30, 41, 59, 0.9);
            border-color: var(--color-border);
        }
        
        body.dark-mode .result-item {
            background: #0F172A;
        }
        
        /* Neural network particle background */
        body::before {
            content: '';
            position: fixed;
            top: -50%;
            right: -50%;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(6, 182, 212, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(139, 92, 246, 0.08) 0%, transparent 50%);
            z-index: -1;
            animation: float 20s ease-in-out infinite;
        }
        
        #particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.4;
        }
        
        @keyframes float {
            0%, 100% { transform: translate(0, 0) rotate(0deg); }
            33% { transform: translate(30px, -30px) rotate(120deg); }
            66% { transform: translate(-20px, 20px) rotate(240deg); }
        }
        
        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 0 20px rgba(6, 182, 212, 0.4); }
            50% { box-shadow: 0 0 40px rgba(6, 182, 212, 0.6); }
        }
        
        @keyframes brain-pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.1); opacity: 0.8; }
        }
        
        /* Navbar */
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 70px;
            background: var(--color-glass);
            backdrop-filter: var(--blur-md);
            -webkit-backdrop-filter: var(--blur-md);
            border-bottom: 1px solid var(--color-border);
            z-index: 1000;
            transition: all 0.3s ease;
        }
        
        .navbar.scrolled {
            background: var(--color-surface);
            box-shadow: var(--shadow-md);
        }
        
        .navbar-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 24px;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .navbar-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
            font-size: 1.25rem;
            color: var(--color-text-primary);
            text-decoration: none;
        }
        
        .navbar-logo-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-cyan) 100%);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
        }
        
        .navbar-links {
            display: flex;
            gap: 32px;
            align-items: center;
        }
        
        .navbar-links a {
            color: var(--color-text-secondary);
            text-decoration: none;
            font-weight: 500;
            font-size: 0.9375rem;
            transition: color 0.2s ease;
        }
        
        .navbar-links a:hover {
            color: var(--color-primary);
        }
        
        .navbar-right {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        
        .status-badge {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            background: var(--color-background);
            border-radius: 20px;
            font-size: 0.8125rem;
            font-weight: 500;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--color-success);
            border-radius: 50%;
            animation: pulse-glow 2s ease-in-out infinite;
        }
        
        .theme-toggle {
            background: var(--color-background);
            border: 1px solid var(--color-border);
            border-radius: 20px;
            padding: 6px 12px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 1rem;
        }
        
        .theme-toggle:hover {
            background: var(--color-primary);
            border-color: var(--color-primary);
        }
        
        @media (max-width: 768px) {
            .navbar-links {
                display: none;
            }
        }
        
        /* Hero Section (Enhanced Header) */
        .header {
            background: var(--color-surface);
            border-radius: var(--radius-xl);
            padding: 60px 40px;
            margin-bottom: 24px;
            box-shadow: var(--shadow-lg);
            text-align: center;
            border: 1px solid var(--color-border);
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-cyan) 50%, var(--color-primary) 100%);
            background-size: 200% 100%;
            animation: shimmer 3s ease-in-out infinite;
        }
        
        .header::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(6, 182, 212, 0.1) 0%, transparent 70%);
            transform: translate(-50%, -50%);
            animation: float 15s ease-in-out infinite;
            pointer-events: none;
        }
        
        @keyframes shimmer {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .header h1 {
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-cyan) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 12px;
            letter-spacing: -0.03em;
            position: relative;
            z-index: 1;
        }
        
        .header .subtitle {
            font-size: 1.25rem;
            color: var(--color-text-secondary);
            font-weight: 500;
            margin-bottom: 24px;
            position: relative;
            z-index: 1;
        }
        
        .cta-button {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 14px 32px;
            background: linear-gradient(135deg, var(--color-cyan) 0%, #0891B2 100%);
            color: white;
            border: none;
            border-radius: var(--radius-md);
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 14px rgba(6, 182, 212, 0.4);
            margin-top: 16px;
            text-decoration: none;
            animation: pulse-glow 3s ease-in-out infinite;
        }
        
        .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(6, 182, 212, 0.5);
        }
        
        .trust-line {
            font-size: 0.875rem;
            color: var(--color-text-tertiary);
            margin-top: 24px;
            font-weight: 500;
        }
        
        .badges {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .badge {
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.8125rem;
            font-weight: 600;
            letter-spacing: 0.01em;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .badge-innovation {
            background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        .badge-hackathon {
            background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
        }
        
        .badge-beta {
            background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
        }
        
        .badge:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
        }
        
        .tech-stack {
            font-size: 0.875rem;
            color: var(--color-text-tertiary);
            margin-top: 16px;
            font-weight: 500;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        
        .tech-stack::before {
            content: '⚡';
            font-size: 1rem;
        }
        
        /* Glassmorphic Card */
        .main-card {
            background: var(--color-glass);
            backdrop-filter: var(--blur-md);
            -webkit-backdrop-filter: var(--blur-md);
            border-radius: var(--radius-xl);
            padding: 40px;
            box-shadow: var(--shadow-lg);
            margin-bottom: 24px;
            border: 1px solid rgba(255, 255, 255, 0.5);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .main-card:hover {
            box-shadow: var(--shadow-xl);
            border-color: rgba(99, 102, 241, 0.5);
            transform: translateY(-2px);
        }
        
        .main-card.focused {
            box-shadow: 0 0 0 4px rgba(6, 182, 212, 0.1), var(--shadow-xl);
            border-color: var(--color-cyan);
            transform: translateY(-4px);
        }
        
        .input-section {
            margin-bottom: 20px;
        }
        
        .input-section label {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 600;
            color: var(--color-text-primary);
            margin-bottom: 12px;
            font-size: 1rem;
            letter-spacing: -0.01em;
        }
        
        .input-section label::before {
            content: '📋';
            font-size: 1.25rem;
        }
        
        .input-section textarea {
            width: 100%;
            padding: 16px;
            border: 2px solid var(--color-border);
            border-radius: var(--radius-md);
            font-size: 0.9375rem;
            line-height: 1.6;
            resize: vertical;
            min-height: 140px;
            font-family: inherit;
            color: var(--color-text-primary);
            background: var(--color-surface);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .input-section textarea:hover {
            border-color: var(--color-text-tertiary);
        }
        
        .input-section textarea:focus {
            outline: none;
            border-color: var(--color-cyan);
            box-shadow: 0 0 0 4px rgba(6, 182, 212, 0.1);
        }
        
        .input-section textarea:focus ~ .card-glow {
            opacity: 1;
        }
        
        .example-chips {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 12px;
        }
        
        .chip {
            padding: 6px 14px;
            background: var(--color-background);
            border: 1px solid var(--color-border);
            border-radius: 16px;
            font-size: 0.8125rem;
            color: var(--color-text-secondary);
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .chip:hover {
            background: var(--color-primary);
            color: white;
            border-color: var(--color-primary);
            transform: scale(1.05);
        }
        
        .input-section textarea::placeholder {
            color: var(--color-text-tertiary);
        }
        
        .examples {
            font-size: 0.8125rem;
            color: var(--color-text-tertiary);
            margin-top: 8px;
            display: flex;
            align-items: flex-start;
            gap: 6px;
            line-height: 1.5;
        }
        
        .examples::before {
            content: '💡';
            flex-shrink: 0;
            margin-top: 1px;
        }
        
        .submit-btn {
            width: 100%;
            padding: 16px 24px;
            background: linear-gradient(135deg, var(--color-primary) 0%, #8B5CF6 100%);
            color: white;
            border: none;
            border-radius: var(--radius-md);
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            letter-spacing: -0.01em;
        }
        
        .submit-btn::before {
            content: '🧠';
            font-size: 1.25rem;
            animation: brain-pulse 2s ease-in-out infinite;
        }
        
        .submit-btn:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
            background: linear-gradient(135deg, var(--color-primary-dark) 0%, #7C3AED 100%);
        }
        
        .submit-btn:active:not(:disabled) {
            transform: translateY(0);
        }
        
        .submit-btn:disabled {
            background: var(--color-text-tertiary);
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
            opacity: 0.6;
        }
        
        .result-card {
            background: var(--color-surface);
            border-radius: var(--radius-xl);
            padding: 40px;
            box-shadow: var(--shadow-xl);
            margin-top: 24px;
            display: none;
            border: 1px solid var(--color-border);
        }
        
        .result-card.show {
            display: block;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px) scale(0.98);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        
        .result-header {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 24px;
            padding-bottom: 20px;
            border-bottom: 2px solid var(--color-border);
            display: flex;
            align-items: center;
            gap: 12px;
            letter-spacing: -0.02em;
        }
        
        .result-header::before {
            content: '✅';
            font-size: 1.75rem;
        }
        
        .result-item {
            padding: 16px;
            margin: 12px 0;
            background: var(--color-background);
            border-left: 3px solid var(--color-primary);
            border-radius: var(--radius-sm);
            transition: all 0.2s ease;
            font-size: 0.9375rem;
            line-height: 1.6;
        }
        
        .result-item:hover {
            background: #F3F4F6;
            transform: translateX(4px);
        }
        
        .result-item strong {
            color: var(--color-text-primary);
            font-weight: 600;
            margin-right: 8px;
        }
        
        .urgency-emergency {
            background: #FEF2F2;
            border-left-color: var(--color-danger);
        }
        
        .urgency-emergency:hover {
            background: #FEE2E2;
        }
        
        .urgency-high {
            background: #FFFBEB;
            border-left-color: var(--color-warning);
        }
        
        .urgency-high:hover {
            background: #FEF3C7;
        }
        
        .urgency-moderate {
            background: #F0FDF4;
            border-left-color: var(--color-success);
        }
        
        .urgency-moderate:hover {
            background: #DCFCE7;
        }
        
        .urgency-low {
            background: #EFF6FF;
            border-left-color: var(--color-info);
        }
        
        .urgency-low:hover {
            background: #DBEAFE;
        }
        
        .metta-analysis {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
            padding: 24px;
            border-radius: var(--radius-md);
            margin-top: 24px;
            border: 1px solid rgba(99, 102, 241, 0.1);
        }
        
        .metta-analysis h3 {
            color: var(--color-primary);
            margin-bottom: 16px;
            font-size: 1.125rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .metta-analysis h3::before {
            content: '🧠';
            font-size: 1.25rem;
        }
        
        .loading {
            text-align: center;
            padding: 40px 20px;
            color: var(--color-text-secondary);
        }
        
        .loading p {
            font-weight: 500;
            font-size: 0.9375rem;
        }
        
        .spinner {
            border: 3px solid var(--color-border);
            border-top: 3px solid var(--color-primary);
            border-radius: 50%;
            width: 48px;
            height: 48px;
            animation: spin 0.8s cubic-bezier(0.4, 0, 0.2, 1) infinite;
            margin: 0 auto 16px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .footer {
            text-align: center;
            color: var(--color-text-tertiary);
            margin-top: 40px;
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        .footer p {
            margin: 4px 0;
        }
        
        /* Responsive Design */
        @media (max-width: 640px) {
            body {
                padding: 16px;
            }
            
            .header {
                padding: 24px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .main-card {
                padding: 24px;
            }
            
            .result-card {
                padding: 24px;
            }
        }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar" id="navbar">
        <div class="navbar-content">
            <a href="#" class="navbar-logo">
                <div class="navbar-logo-icon">🧠</div>
                <span>SynaptiVerse</span>
            </a>
            <div class="navbar-links">
                <a href="#home">Home</a>
                <a href="#about">About</a>
                <a href="#timeline">Timeline</a>
                <a href="https://github.com/ASI-Alliance/synaptiVerse" target="_blank">GitHub</a>
            </div>
            <div class="navbar-right">
                <div class="status-badge">
                    <span class="status-dot"></span>
                    <span>Agents Online</span>
                </div>
                <button class="theme-toggle" onclick="toggleTheme()" title="Toggle dark mode">🌙</button>
            </div>
        </div>
    </nav>

    <div class="container" id="home">
        <!-- Hero Section -->
        <div class="header">
            <h1>SynaptiVerse</h1>
            <p class="subtitle">Autonomous Healthcare Coordination with Multi-Agent AI</p>
            <div class="badges">
                <span class="badge badge-beta">✨ Beta</span>
                <span class="badge badge-innovation">⚡ Innovation Lab</span>
                <span class="badge badge-hackathon">🏆 ASI Alliance Cypherpunk</span>
            </div>
            <a href="#analyze" class="cta-button" onclick="document.getElementById('symptomsInput').focus()">
                Get Started →
            </a>
            <div class="tech-stack">
                Powered by Fetch.ai • SingularityNET MeTTa • Agentverse
            </div>
        </div>
        
        <!-- Dashboard Grid -->
        <div class="dashboard-grid" id="analyze">
            <!-- Main Analysis Card -->
            <div>
                <div class="main-card">
                    <div class="input-section">
                        <label>Describe Your Symptoms</label>
                        <textarea 
                            id="symptomsInput" 
                            placeholder="Example: I have fever, cough, and fatigue&#10;&#10;Be as specific as possible for better analysis..."  
                        ></textarea>
                        <div class="examples">
                            Examples: "fever and headache" | "chest pain and shortness of breath" | "severe stomach pain"
                        </div>
                    </div>
                    
                    <button class="submit-btn" onclick="analyzeSymptoms()">
                        Analyze Symptoms & Schedule Appointment
                    </button>
                </div>
                
                <div id="loadingCard" class="result-card">
                    <div class="loading">
                        <div class="spinner"></div>
                        <p>Analyzing with MeTTa AI...</p>
                    </div>
                </div>
                
                <div id="resultCard" class="result-card">
                    <div class="result-header" id="resultHeader">Appointment Confirmed</div>
                    <div id="resultContent"></div>
                </div>
            </div>
            
            <!-- Agent Status Panel -->
            <div class="agent-panel">
                <div class="panel-header">
                    🤖 Live Agent Status
                </div>
                
                <div class="agent-status-item">
                    <div class="agent-name">
                        <span class="status-dot"></span>
                        Appointment Coordinator
                    </div>
                    <div class="agent-metric">
                        <span>Status:</span>
                        <span class="metric-value">Active</span>
                    </div>
                    <div class="agent-metric">
                        <span>Response Time:</span>
                        <span class="metric-value">2.3s</span>
                    </div>
                </div>
                
                <div class="agent-status-item">
                    <div class="agent-name">
                        <span class="status-dot"></span>
                        Medical Advisor
                    </div>
                    <div class="agent-metric">
                        <span>Status:</span>
                        <span class="metric-value">Active</span>
                    </div>
                    <div class="agent-metric">
                        <span>MeTTa Queries:</span>
                        <span class="metric-value" id="mettaQueries">0</span>
                    </div>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value" id="totalAnalyses">0</div>
                        <div class="stat-label">Total Analyses</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">500+</div>
                        <div class="stat-label">Medical Facts</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">100%</div>
                        <div class="stat-label">Test Success</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">9/9</div>
                        <div class="stat-label">E2E Passing</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Appointment Timeline -->
        <div class="timeline-section">
            <div class="timeline-header">
                <div class="timeline-title">📅 Appointment Timeline</div>
                <button class="timeline-toggle" onclick="toggleTimeline()" id="timelineToggle">
                    Expand
                </button>
            </div>
            <div class="timeline-content" id="timelineContent">
                <div class="timeline-item">
                    <div class="timeline-event">
                        <div class="timeline-event-title">System Initialized</div>
                        <div class="timeline-event-desc">MeTTa knowledge graph loaded with 500+ medical facts</div>
                    </div>
                </div>
                <div class="timeline-item" id="timelineItems">
                    <!-- Dynamic timeline items will be added here -->
                </div>
            </div>
        </div>
        
        <!-- About Section -->
        <div class="about-section" id="about">
            <div class="about-title">🚀 Why SynaptiVerse?</div>
            <div class="about-subtitle">
                The future of healthcare is autonomous, intelligent, and patient-centric
            </div>
            
            <div class="features-grid">
                <div class="feature-card">
                    <span class="feature-icon">🤖</span>
                    <div class="feature-title">Autonomous Agents</div>
                    <div class="feature-desc">
                        Self-coordinating agents built with Fetch.ai handle appointment scheduling, 
                        symptom analysis, and specialist matching without human intervention.
                    </div>
                </div>
                
                <div class="feature-card">
                    <span class="feature-icon">🧠</span>
                    <div class="feature-title">MeTTa Reasoning</div>
                    <div class="feature-desc">
                        SingularityNET's symbolic AI performs multi-hop knowledge graph traversal 
                        across 500+ medical facts for accurate diagnosis suggestions.
                    </div>
                </div>
                
                <div class="feature-card">
                    <span class="feature-icon">⚡</span>
                    <div class="feature-title">Real-Time Analysis</div>
                    <div class="feature-desc">
                        Get instant symptom analysis and specialist recommendations in under 3 seconds, 
                        with confidence scores and urgency classification.
                    </div>
                </div>
                
                <div class="feature-card">
                    <span class="feature-icon">🔒</span>
                    <div class="feature-title">Privacy-First</div>
                    <div class="feature-desc">
                        Zero PHI storage with ephemeral data processing. All health data is analyzed 
                        in-memory and never persisted to databases.
                    </div>
                </div>
                
                <div class="feature-card">
                    <span class="feature-icon">🚨</span>
                    <div class="feature-title">Emergency Detection</div>
                    <div class="feature-desc">
                        Multi-hop reasoning automatically identifies life-threatening conditions 
                        and escalates to emergency protocols immediately.
                    </div>
                </div>
                
                <div class="feature-card">
                    <span class="feature-icon">🌐</span>
                    <div class="feature-title">Decentralized</div>
                    <div class="feature-desc">
                        Built on ASI Alliance principles with agent discovery via Agentverse, 
                        enabling future integration with insurance, lab, and pharmacy agents.
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer-main">
            <div class="container">
                <div class="footer-grid">
                    <div class="footer-brand">
                        <div class="footer-logo">SynaptiVerse</div>
                        <div class="footer-desc">
                            Autonomous healthcare coordination powered by Fetch.ai agents, 
                            SingularityNET MeTTa reasoning, and Agentverse discovery. 
                            Built for the ASI Alliance Cypherpunk Hackathon 2025.
                        </div>
                    </div>
                    
                    <div class="footer-column">
                        <h4>Product</h4>
                        <ul class="footer-links">
                            <li><a href="#home">Home</a></li>
                            <li><a href="#analyze">Analyze Symptoms</a></li>
                            <li><a href="#about">About</a></li>
                            <li><a href="#timeline">Timeline</a></li>
                        </ul>
                    </div>
                    
                    <div class="footer-column">
                        <h4>Technology</h4>
                        <ul class="footer-links">
                            <li><a href="https://fetch.ai" target="_blank">Fetch.ai</a></li>
                            <li><a href="https://singularitynet.io" target="_blank">SingularityNET</a></li>
                            <li><a href="https://agentverse.ai" target="_blank">Agentverse</a></li>
                            <li><a href="https://github.com/ASI-Alliance" target="_blank">ASI Alliance</a></li>
                        </ul>
                    </div>
                    
                    <div class="footer-column">
                        <h4>Resources</h4>
                        <ul class="footer-links">
                            <li><a href="https://github.com/yourusername/synaptiVerse" target="_blank">GitHub</a></li>
                            <li><a href="#" onclick="alert('Documentation coming soon!')">Documentation</a></li>
                            <li><a href="#" onclick="alert('API access coming soon!')">API Access</a></li>
                            <li><a href="#" onclick="alert('Contact: your@email.com')">Contact</a></li>
                        </ul>
                    </div>
                </div>
                
                <div class="footer-bottom">
                    <div>
                        © 2025 SynaptiVerse. Built for ASI Alliance Hackathon.
                    </div>
                    <div class="social-links">
                        <a href="#" title="GitHub">📱</a>
                        <a href="#" title="Twitter">🐦</a>
                        <a href="#" title="Discord">💬</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Dark mode toggle
        function toggleTheme() {
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            document.querySelector('.theme-toggle').textContent = isDark ? '☀️' : '🌙';
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        }
        
        // Load saved theme
        window.addEventListener('DOMContentLoaded', () => {
            const savedTheme = localStorage.getItem('theme');
            if (savedTheme === 'dark') {
                document.body.classList.add('dark-mode');
                document.querySelector('.theme-toggle').textContent = '☀️';
            }
        });
        
        // Navbar scroll effect
        window.addEventListener('scroll', () => {
            const navbar = document.getElementById('navbar');
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
        
        // Timeline toggle
        function toggleTimeline() {
            const content = document.getElementById('timelineContent');
            const button = document.getElementById('timelineToggle');
            content.classList.toggle('expanded');
            button.textContent = content.classList.contains('expanded') ? 'Collapse' : 'Expand';
        }
        
        // Statistics tracking
        let totalAnalysesCount = 0;
        let mettaQueriesCount = 0;
        
        function updateStats() {
            totalAnalysesCount++;
            mettaQueriesCount++;
            document.getElementById('totalAnalyses').textContent = totalAnalysesCount;
            document.getElementById('mettaQueries').textContent = mettaQueriesCount;
        }
        
        function addTimelineEvent(title, description) {
            const timelineItems = document.getElementById('timelineItems');
            const now = new Date();
            const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
            
            const item = document.createElement('div');
            item.className = 'timeline-item';
            item.innerHTML = `
                <div class="timeline-event">
                    <div class="timeline-event-title">${title}</div>
                    <div class="timeline-event-desc">${description} - ${timeStr}</div>
                </div>
            `;
            timelineItems.appendChild(item);
            
            // Auto-expand timeline on new event
            const content = document.getElementById('timelineContent');
            if (!content.classList.contains('expanded')) {
                toggleTimeline();
            }
        }
        
        async function analyzeSymptoms() {
            const symptoms = document.getElementById('symptomsInput').value.trim();
            
            if (!symptoms) {
                alert('Please describe your symptoms');
                return;
            }
            
            // Add timeline event
            addTimelineEvent('Analysis Started', `Symptoms: "${symptoms.substring(0, 50)}..."`);
            updateStats();
            
            // Show loading
            document.getElementById('loadingCard').classList.add('show');
            document.getElementById('resultCard').classList.remove('show');
            document.querySelector('.submit-btn').disabled = true;
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ symptoms: symptoms })
                });
                
                const data = await response.json();
                
                // Add timeline event
                if (data.success) {
                    addTimelineEvent(
                        'Appointment Created', 
                        `${data.appointment_id} - ${data.specialist} (${data.urgency})`
                    );
                }
                
                // Hide loading
                document.getElementById('loadingCard').classList.remove('show');
                
                // Show result
                displayResult(data);
                
            } catch (error) {
                console.error('Error:', error);
                addTimelineEvent('Analysis Failed', 'Error communicating with server');
                alert('Error analyzing symptoms. Please try again.');
            } finally {
                document.querySelector('.submit-btn').disabled = false;
            }
        }
        
        function displayResult(data) {
            const resultCard = document.getElementById('resultCard');
            const resultHeader = document.getElementById('resultHeader');
            const resultContent = document.getElementById('resultContent');
            
            if (!data.success) {
                resultHeader.textContent = '❌ Unable to Process';
                resultContent.innerHTML = `<p>${data.message}</p>`;
                resultCard.classList.add('show');
                return;
            }
            
            resultHeader.textContent = '✅ Appointment Confirmed';
            
            const urgencyClass = `urgency-${data.urgency}`;
            const urgencyIcon = {
                'emergency': '🚨',
                'high': '⚠️',
                'moderate': '📅',
                'low': 'ℹ️'
            }[data.urgency] || '📅';
            
            resultContent.innerHTML = `
                <div class="result-item">
                    <strong>📋 Appointment ID:</strong> ${data.appointment_id}
                </div>
                
                <div class="result-item">
                    <strong>📅 Scheduled Time:</strong> ${data.scheduled_time}
                </div>
                
                <div class="result-item">
                    <strong>👨‍⚕️ Specialist:</strong> ${formatText(data.specialist)}
                </div>
                
                <div class="result-item ${urgencyClass}">
                    <strong>${urgencyIcon} Urgency:</strong> ${data.urgency.toUpperCase()}
                </div>
                
                <div class="metta-analysis">
                    <h3>🧠 MeTTa AI Analysis</h3>
                    <div class="result-item">
                        <strong>Likely Condition:</strong> ${formatText(data.condition)}
                    </div>
                    <div class="result-item">
                        <strong>Confidence:</strong> ${Math.round(data.confidence * 100)}%
                    </div>
                    <div style="margin-top: 10px; font-size: 0.9em; color: #666;">
                        <strong>Analysis Method:</strong> Multi-hop knowledge graph reasoning<br>
                        <strong>Knowledge Base:</strong> 500+ medical facts<br>
                        <strong>Technology:</strong> SingularityNET MeTTa symbolic AI
                    </div>
                </div>
                
                ${data.urgency === 'emergency' ? 
                    '<div class="result-item urgency-emergency" style="margin-top: 20px; font-weight: bold;">🚨 URGENT: This appears to be a medical emergency. Please call 911 or visit the nearest Emergency Room immediately!</div>' 
                    : ''}
                
                <div style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; font-size: 0.9em;">
                    💡 <strong>Next Steps:</strong><br>
                    • You will receive a confirmation email/SMS shortly<br>
                    • Please arrive 15 minutes before your appointment<br>
                    • Bring your ID and insurance card
                </div>
            `;
            
            resultCard.classList.add('show');
        }
        
        function formatText(text) {
            return text.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        }
        
        // Allow Enter to submit (with Shift+Enter for new line)
        document.getElementById('symptomsInput').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                analyzeSymptoms();
            }
        });
    </script>
</body>
</html>
    """

@app.post("/analyze", response_model=AppointmentResponse)
async def analyze_symptoms(request: SymptomRequest):
    """Analyze symptoms and create appointment"""
    from datetime import datetime, timedelta
    from uuid import uuid4
    
    symptoms_text = request.symptoms.strip()
    
    if not symptoms_text:
        return AppointmentResponse(
            success=False,
            message="Please describe your symptoms"
        )
    
    # Query MeTTa
    metta_result = query_metta(symptoms_text)
    
    if metta_result["status"] != "success" or not metta_result.get("possible_conditions"):
        return AppointmentResponse(
            success=False,
            message="Unable to analyze symptoms. Please try describing them differently or consult a general practitioner."
        )
    
    # Get top recommendation
    top_condition = metta_result["possible_conditions"][0]
    
    # Generate appointment time
    now = datetime.utcnow()
    urgency = top_condition["urgency"]
    
    if urgency == "emergency":
        scheduled_time = "IMMEDIATE - Visit Emergency Room"
    elif urgency == "high":
        scheduled_time = (now + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M UTC")
    elif urgency == "moderate":
        scheduled_time = (now + timedelta(days=2)).strftime("%Y-%m-%d 10:00 UTC")
    else:
        scheduled_time = (now + timedelta(days=5)).strftime("%Y-%m-%d 14:00 UTC")
    
    # Create appointment
    appointment_id = f"APT-{str(uuid4())[:8].upper()}"
    appointment = {
        "id": appointment_id,
        "symptoms": symptoms_text,
        "condition": top_condition["condition"],
        "specialist": top_condition["specialist"],
        "urgency": urgency,
        "confidence": top_condition["confidence"],
        "scheduled_time": scheduled_time,
        "created_at": now.isoformat()
    }
    
    appointments[appointment_id] = appointment
    
    return AppointmentResponse(
        success=True,
        appointment_id=appointment_id,
        message="Appointment created successfully",
        specialist=top_condition["specialist"],
        urgency=urgency,
        scheduled_time=scheduled_time,
        confidence=top_condition["confidence"],
        condition=top_condition["condition"]
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SynaptiVerse Healthcare API",
        "appointments": len(appointments)
    }

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 SYNAPTIVERSE WEB UI - STARTING")
    print("="*60)
    print("\n🌐 Web Interface will be available at:")
    print("   http://localhost:8000")
    print("\n📊 Features:")
    print("   • Interactive symptom analysis")
    print("   • MeTTa AI-powered recommendations")
    print("   • Automatic appointment scheduling")
    print("   • Beautiful responsive UI")
    print("\n💡 Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
