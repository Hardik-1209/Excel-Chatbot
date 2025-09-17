# Deployment Guide

This guide provides instructions for deploying the NL to SQL Chatbot application on Render (backend) and Vercel (frontend).

## Backend Deployment on Render

### Option 1: Deploy using render.yaml (Recommended)

1. **Create a Render Account**
   - Sign up at [render.com](https://render.com) if you don't have an account

2. **Deploy using Blueprint**
   - Fork or clone this repository to your GitHub account
   - From the Render dashboard, click "New" and select "Blueprint"
   - Connect your GitHub/GitLab repository
   - Select the repository where you've forked/cloned this project
   - Render will automatically detect the `render.yaml` file
   - Click "Apply Blueprint"

3. **Environment Variables**
   - The `render.yaml` file already includes the necessary environment variables
   - You'll need to manually set the value for `GROQ_API_KEY` in the Render dashboard

4. **Deploy**
   - Render will automatically build and deploy both the backend and frontend services
   - The deployment process may take a few minutes
   - Once deployed, you'll get URLs for both services

### Option 2: Manual Deployment

1. **Create a Render Account**
   - Sign up at [render.com](https://render.com) if you don't have an account

2. **Create a New Web Service**
   - From the Render dashboard, click "New" and select "Web Service"
   - Connect your GitHub/GitLab repository or use the "Public Git repository" option
   - Enter the repository URL where your backend code is hosted

3. **Configure the Web Service**
   - Name: `data-analysis-api` (or your preferred name)
   - Environment: `Python`
   - Branch: `main` (or your default branch)
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Click "Create Web Service"

4. **Environment Variables**
   - In the web service dashboard, go to "Environment" tab
   - Add the following environment variables:
     - `GROQ_API_KEY`: Your Groq API key
     - `PORT`: `10000` (Render will automatically set this, but you can specify it)

5. **Deploy**
   - Render will automatically build and deploy your application
   - The deployment process may take a few minutes
   - Once deployed, you'll get a URL like `https://data-analysis-api.onrender.com`

## Frontend Deployment

### Option 1: Deploy Frontend on Render (Using render.yaml)

If you used the render.yaml blueprint deployment method for the backend, your frontend will be automatically deployed as well. The render.yaml file configures both services.

1. **Environment Variables**
   - The frontend service is configured to automatically get the backend URL
   - No manual configuration is needed for the API URL

2. **Verify Deployment**
   - Once deployed, Render will provide a URL for your frontend service
   - Open the URL in your browser to verify the deployment

### Option 2: Deploy Frontend on Vercel

If you prefer to deploy the frontend separately on Vercel:

1. **Create a Vercel Account**
   - Sign up at [vercel.com](https://vercel.com) if you don't have an account

2. **Install Vercel CLI (Optional)**
   - Run `npm install -g vercel` to install the Vercel CLI

3. **Prepare Your Frontend**
   - Create a `.env.production` file in your frontend directory with:
     ```
     REACT_APP_API_URL=https://your-render-backend-url.onrender.com
     ```
   - Replace with your actual Render backend URL

4. **Deploy to Vercel**
   - **Option 1: Using Vercel Dashboard**
     - From the Vercel dashboard, click "New Project"
     - Import your Git repository
     - Configure project settings:
       - Framework Preset: React
       - Build Command: `npm run build`
       - Output Directory: `build`
       - Environment Variables: Add `REACT_APP_API_URL` with your backend URL
     - Click "Deploy"

   - **Option 2: Using Vercel CLI**
     - Navigate to your frontend directory
     - Run `vercel` and follow the prompts
     - For production deployment, run `vercel --prod`

5. **Verify Deployment**
   - Once deployed, Vercel will provide a URL for your frontend
   - Open the URL in your browser to verify the deployment

## Connecting Frontend and Backend

1. **CORS Configuration**
   - The backend is already configured to accept requests from any origin
   - If you need to restrict this, update the CORS configuration in `app.py`

2. **Testing the Connection**
   - Upload a file through the frontend interface
   - Verify that the file is processed and stored in the backend
   - Test natural language queries to ensure they're properly converted to SQL

## Troubleshooting

- **Backend Issues**
  - Check Render logs for any errors
  - Verify environment variables are correctly set
  - Ensure the Groq API key is valid

- **Frontend Issues**
  - Check browser console for any errors
  - Verify the backend URL is correctly set in environment variables
  - Check network requests to ensure they're reaching the backend

- **File Upload Issues**
  - Verify file size limits (Render free tier has limitations)
  - Check file format compatibility

## Maintenance

- **Scaling**
  - For larger datasets, consider upgrading to a paid Render plan
  - For PostgreSQL integration, update the database connection in `app.py`

- **Monitoring**
  - Use Render's built-in monitoring tools
  - Consider implementing additional logging for production use