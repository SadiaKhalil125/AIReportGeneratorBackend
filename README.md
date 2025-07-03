# GenAI Report Generator

<div align="center">
  <h3>🤖 AI-Powered Research Report Generator</h3>
  <p>Generate comprehensive, professional research reports on any topic using OpenAI's GPT models</p>
  
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
  [![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
  [![TypeScript](https://img.shields.io/badge/TypeScript-4.7.4-blue.svg)](https://www.typescriptlang.org/)
  [![Material-UI](https://img.shields.io/badge/Material--UI-7.2.0-blue.svg)](https://mui.com/)
  [![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--turbo-orange.svg)](https://openai.com/)
</div>

## 🌟 Features

- **🤖 AI-Powered Content Generation**: Leverages OpenAI's GPT models to create comprehensive research reports
- **📄 PDF Report Generation**: Automatically generates professional PDF reports with custom styling
- **🔐 User Authentication**: Secure JWT-based authentication system
- **💻 Modern UI**: Beautiful, responsive interface built with Material-UI
- **📱 Mobile-Friendly**: Fully responsive design that works on all devices
- **⚡ Real-time Processing**: Fast report generation and download
- **🎨 Professional Styling**: Custom-designed PDF reports with proper formatting

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **OpenAI API**: AI-powered content generation
- **ReportLab**: PDF generation library
- **JWT**: Secure authentication tokens
- **BCrypt**: Password hashing for security

### Frontend
- **React**: User interface library
- **TypeScript**: Type-safe JavaScript
- **Material-UI**: React component library
- **Axios**: HTTP client for API requests
- **React Router**: Client-side routing

### Database
- **SQLite**: Lightweight database for development
- **SQLAlchemy ORM**: Database abstraction layer

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- OpenAI API key (optional - falls back to demo content)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/SadiaKhalil125/AIReportGeneratorFrontend.git
cd AIReportGeneratorFrontend
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env file with your configuration
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create environment file (if needed)
cp .env.example .env.local
```

## ⚙️ Configuration

### Backend Environment Variables
Create a `.env` file in the `backend` directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# JWT Configuration
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# Database Configuration
DATABASE_URL=sqlite:///./genai_reports.db

# Application Settings
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### Frontend Environment Variables
Create a `.env.local` file in the `frontend` directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

## 🏃‍♂️ Running the Application

### Start Backend Server
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend Server
```bash
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📚 API Documentation

### Authentication Endpoints

#### POST `/auth/signup`
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}
```

#### POST `/auth/login`
Authenticate user and receive access token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

#### GET `/auth/me`
Get current user information (requires authentication).

### Report Generation Endpoints

#### POST `/generate-report`
Generate a new AI-powered report.

**Request Body:**
```json
{
  "topic": "Artificial Intelligence in Healthcare"
}
```

**Response:**
```json
{
  "message": "Report generated successfully",
  "filename": "report_username_20240101_120000.pdf",
  "download_url": "/download/report_username_20240101_120000.pdf"
}
```

#### GET `/download/{filename}`
Download a generated report (requires authentication).

### Health Check Endpoints

#### GET `/health`
Check API health status.

## 🎯 Usage

1. **Register/Login**: Create an account or login with existing credentials
2. **Generate Report**: Enter a topic and click "Generate Report"
3. **AI Processing**: The system uses OpenAI's GPT models to create comprehensive content
4. **PDF Generation**: The content is automatically formatted into a professional PDF
5. **Download**: Download your generated report instantly

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for all frontend code
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed

## 📁 Project Structure

```
genai-report-generator/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── auth.py              # Authentication logic
│   ├── models.py            # Database models
│   ├── database.py          # Database configuration
│   ├── ai_service.py        # OpenAI integration
│   ├── pdf_generator.py     # PDF generation
│   ├── config.py            # Configuration settings
│   ├── requirements.txt     # Python dependencies
│   └── reports/             # Generated reports storage
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── contexts/       # React contexts
│   │   ├── services/       # API services
│   │   ├── App.tsx         # Main app component
│   │   └── index.tsx       # Entry point
│   ├── package.json        # Frontend dependencies
│   └── tsconfig.json       # TypeScript configuration
├── README.md               # This file
└── DEPLOYMENT.md          # Deployment instructions
```

## 🔧 Troubleshooting

### Common Issues

1. **OpenAI API Key Issues**
   - Ensure your API key is valid and has sufficient credits
   - The system will fall back to demo content if the API key is invalid

2. **Database Connection Issues**
   - Check if the database file exists and has proper permissions
   - Ensure SQLAlchemy is properly configured

3. **CORS Issues**
   - Make sure the frontend URL is properly configured in the backend CORS settings

4. **Port Conflicts**
   - Check if ports 3000 and 8000 are available
   - Modify the ports in configuration if needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT API
- FastAPI team for the excellent framework
- Material-UI team for the beautiful components
- ReportLab team for PDF generation capabilities

## 📞 Support

If you have any questions or issues, please:
1. Check the [Issues](https://github.com/yourusername/genai-report-generator/issues) page
2. Create a new issue if your problem isn't already reported
3. Provide detailed information about your environment and the issue

---

<div align="center">
  <p>Made with ❤️ by Sadia</p>
  <p>⭐ Star this repo if you find it helpful!</p>
</div>
