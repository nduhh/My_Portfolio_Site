from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.middleware.csrf import get_token
import json
import random

def home(request):
    # Ensure CSRF token is set in cookie
    get_token(request)
    return render(request, "index.html")

def projects(request):
    return render(request, "projects.html")

def about(request):
    return render(request, "about.html")

@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "").lower()
            
            if not message:
                return JsonResponse({"success": False, "reply": "No message provided"}, status=400)

            # Check if OpenAI API key is configured
            api_key = getattr(settings, 'OPENAI_API_KEY', None)
            
            if api_key and api_key not in ["", "your-api-key-here"]:
                # Use OpenAI if key is configured
                try:
                    from openai import OpenAI
                    client = OpenAI(api_key=api_key)
                    
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": """You are an AI assistant for Nduduzo Nkosikhona, 
                             a Full Stack Developer based in South Africa. Answer questions about his skills, 
                             experience, and projects. Keep responses concise and professional."""},
                            {"role": "user", "content": message}
                        ],
                        max_tokens=150
                    )
                    reply = response.choices[0].message.content
                except Exception as e:
                    # Fallback to rule-based if OpenAI fails
                    reply = get_rule_based_response(message)
            else:
                # Use rule-based responses
                reply = get_rule_based_response(message)
            
            return JsonResponse({"success": True, "reply": reply})
            
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "reply": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "reply": str(e)}, status=500)
    
    return JsonResponse({"success": False, "reply": "Only POST requests are allowed"}, status=405)

def get_rule_based_response(message):
    """Rule-based responses for the portfolio assistant"""
    message = message.lower()
    
    # Skills related queries
    if any(word in message for word in ['skill', 'technologies', 'tech stack', 'know']):
            return (
            f"You typed: {message}\n"
            "Respond: Nduduzo specializes in Full Stack Development using Python (Django) for backend "
            "and JavaScript (HTML, CSS, JavaScript) for frontend development. "
            "He also develops mobile applications using React Native and Python (Django). "
            "His expertise includes AI integration, OCR with Google ML Kit, REST APIs, PostgreSQL databases, "
            "and building scalable, production-ready systems."
        )
    
    # Education related
    elif any(word in message for word in ['education', 'study', 'studied', 'university', 'tut', 'school', 'qualification']):
        return (
            f"You typed: {message}\n"
            "Respond: Nduduzo studied Computer Science at Tshwane University of Technology (TUT), "
            "where he completed his Diploma in Computer Science in January 2026 and is graduated that year. "
            "He completed his matric in 2020 at Amandla High School. "
            "His academic background provided strong foundations in programming, systems development, and software engineering."
        )

    # Experience related
    elif any(word in message for word in ['experience', 'background', 'work', 'career']):
        return (
    f"You typed: {message}\n"
    "Response: Nduduzo completed his Work Integrated Learning (WIL) as a Software Developer "
    "at NSK IT Solutions. During this period, he independently developed a full internal "
    "intranet web application with role-based access control. He was responsible for "
    "system analysis, planning, documentation, development, testing, and deployment.\n\n"
    "He also worked with Fluid Intellect on a school-based project, where he contributed "
    "as a Frontend Developer, building user interfaces and implementing interactive features."
        )
    
    # Projects related
    elif any(word in message for word in ['project', 'portfolio', 'build', 'developed']):
        return (
            f"You typed: {message}\n"
            "Respond: Nduduzo has built multiple real-world projects including:"
            "• An AI-powered portfolio chatbot using Django, HTML, CSS, and JavaScript\n"
            "• A React Native OCR scanner with live text recognition\n"
            "• An AR mobile application called Lumora developed for Fluid Intellect, "
            "which scans insurance documents and overlays explanations using AI\n"
            "• A navigation app using Google Maps API and OpenStreetMap (personal ongoing project)\n"
            "• A company intranet system with role-based access control for NSK IT Solutions\n"
        )    
    # Contact related
    elif any(word in message for word in ['contact', 'reach', 'email']):
        return (
            f"You typed: {message}\n"
            "Respond: You can contact Nduduzo through the contact form on this website or connect with him on LinkedIn."
        )    

    # AI related
    elif any(word in message for word in ['ai', 'machine learning', 'ocr', 'artificial intelligence']):
        return (
            f"You typed: {message}\n"
            "Respond: Nduduzo actively works with Artificial Intelligence technologies including "
            "Optical Character Recognition (OCR) using Google ML Kit, GPT integrations, "
            "and intelligent chatbot systems. He focuses on building practical AI-powered "
            "applications that solve real-world problems."
        )

    # Hiring / Why hire
    elif any(word in message for word in ['hire', 'why', 'employ', 'recruit']):
        return (
            f"You typed: {message}\n"
            "Respond: Nduduzo combines strong backend architecture skills with modern frontend and AI integration. "
            "He has real-world experience delivering complete systems independently — from analysis "
            "and design to deployment. He is analytical, adaptable, and passionate about building "
            "innovative and scalable solutions."
        )

    # Mobile development
    elif any(word in message for word in ['mobile', 'android', 'react native']):
        return (
            f"You typed: {message}\n"
            "Respond: Nduduzo develops cross-platform mobile applications using React Native and Django. "
            "He has experience integrating native Android modules, implementing camera-based OCR scanning, "
            "and building performance-optimized mobile solutions."
        )

    # Location related
    elif any(word in message for word in ['south africa', 'location', 'based', 'where']):
        return (
            f"You typed: {message}\n"
            "Respond: Nduduzo is based in South Africa and works with clients both locally and internationally.")
    
    # Greetings
    elif any(word in message for word in ['hello', 'hi', 'hey', 'greetings']):
        return (
            f"You typed: {message}\n"
            "Respond: Hello! I'm Nduduzo's AI assistant. How can I help you learn more about his work today?")
    
    # Default response
    else:
        responses = [
            f"You typed: {message}\n"
            "Respond: That's an interesting question about Nduduzo's work. Could you be more specific?",
            "I'd be happy to help you learn more about Nduduzo's skills and experience. What would you like to know?",
            "Nduduzo specializes in full-stack development and AI integration. Feel free to ask about his specific skills or projects.",
            "I'm here to AI questions about Nduduzo's professional background. What are you interested in?"
        ]
        return random.choice(responses)