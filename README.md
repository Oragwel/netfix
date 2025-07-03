# NetFix

## Overview
NetFix is a modern web platform designed to connect **customers** with **companies** providing various home services. Whether it's **plumbing, interior design, housekeeping, or electrical work**, customers can seamlessly request services, and companies can manage their offerings with a professional, user-friendly interface.

## ✨ Key Features

### 🔐 **Advanced User Authentication**
- **Dual Registration System**: Separate registration flows for customers and companies
- **Email-based Login**: Secure authentication using email addresses
- **Service Preservation**: Selected services are preserved during login/registration flow
- **Profile Management**: Comprehensive profile pages with statistics and service history
- **Access Control**: Protected routes with proper authentication decorators

### 🏢 **Company Management**
- **Specialized Services**: Companies create services based on their field of work
- **All-in-One Support**: "All in One" companies can offer services across all categories
- **Service Analytics**: Companies can view customer requests, revenue, and statistics
- **Professional Profiles**: Beautiful company profiles with service showcases
- **Request Management**: Companies can view and manage customer service requests

### 👥 **Customer Experience**
- **Service Discovery**: Browse services by category or view all services
- **Most Requested**: Dedicated section for popular services
- **Detailed Service Pages**: Comprehensive service information with pricing
- **Request History**: Track all service requests with cost calculations
- **Profile Statistics**: View membership duration and request history

### 🛠 **Service Management**
- **Category-based Organization**: 11 service categories (Plumbing, Electricity, etc.)
- **Dynamic Pricing**: Hourly rate system with duration-based cost calculation
- **Service Requests**: Customers specify address and service duration
- **Request Tracking**: Complete history with provider details and costs
- **Real-time Statistics**: Most requested services and trending categories

### 🎨 **Modern UI/UX**
- **Cool Blue Theme**: Professional, consistent color scheme throughout
- **Glass Morphism Design**: Modern visual effects with backdrop blur
- **Responsive Navigation**: Optimized for both desktop and mobile devices
- **Intuitive Layout**: Clean, professional interface with smooth interactions
- **Enhanced Forms**: Beautiful form styling with proper validation and error handling

## Tech Stack
- **Backend**: Django 3.1.14 (Python)
- **Database**: PostgreSQL (or SQLite for local development)
- **Caching & Optimization**: Redis (optional)
- **Authentication**: Django’s built-in system

## Documentation

For detailed technical documentation, see the [docs/](docs/) folder:
- **[Service Structure](docs/SERVICE_STRUCTURE_SUMMARY.md)** - Service model and field definitions
- **[Feature Implementation](docs/SERVICE_PAGES_SUMMARY.md)** - Service browsing and request system
- **[System Architecture](docs/FIELD_RESTRICTIONS_DEMO.md)** - Company restrictions and validation rules

## 🚀 Recent Major Updates

### **Service Preservation System** *(Latest)*
- **Seamless Authentication Flow**: Users no longer lose their selected service when logging in or registering
- **Smart Redirects**: Automatic return to the original service page after authentication
- **Enhanced UX**: Complete user journey from service discovery to request without interruption

### **Navigation Improvements**
- **Restructured Menu**: Moved 'All Services' and 'Most Requested' to main navigation bar
- **Service Categories Dropdown**: Organized individual service categories in a clean dropdown
- **Responsive Design**: Optimized navigation width for company users with additional menu items
- **Mobile Optimization**: Progressive spacing and font size adjustments for different screen sizes

### **Visual Design Overhaul**
- **Cool Blue Theme**: Professional, consistent color scheme replacing previous designs
- **Modern Styling**: Glass morphism effects with backdrop blur throughout the application
- **Enhanced Forms**: Beautiful form styling matching the overall design language
- **Improved Profiles**: Redesigned customer and company profile pages with better information display

### **Authentication Enhancements**
- **Login Page Redesign**: Updated to match registration page styling with consistent theme
- **Better Error Handling**: Improved form validation and error message display
- **Profile Statistics**: Enhanced membership duration display with readable format
- **Access Control**: Proper login redirects and protected route handling

## 🏗 Project Structure

```
netfix/
├── main/                   # Core application and homepage
├── users/                  # User authentication and profiles
│   ├── models.py          # User, Customer, Company models
│   ├── views.py           # Authentication and profile views
│   └── templates/         # Login, registration, profile templates
├── services/              # Service management system
│   ├── models.py          # Service and ServiceRequest models
│   ├── views.py           # Service CRUD and request handling
│   └── templates/         # Service pages and forms
├── static/                # CSS, JavaScript, and images
│   └── css/
│       └── style.css      # Main stylesheet with modern design
├── docs/                  # Technical documentation
└── manage.py              # Django management script
```

## 🎯 Service Categories

NetFix supports 11 comprehensive service categories:
- **🔧 Plumbing** - Water systems, pipes, and fixtures
- **⚡ Electricity** - Electrical installations and repairs
- **🎨 Painting** - Interior and exterior painting services
- **🌿 Gardening** - Landscaping and garden maintenance
- **🏠 Housekeeping** - Cleaning and maintenance services
- **🪑 Carpentry** - Furniture and woodwork services
- **❄️ Air Conditioner** - HVAC installation and maintenance
- **🔒 Locks** - Security and lock services
- **🏡 Interior Design** - Home decoration and design
- **🔧 Home Machines** - Appliance repair and maintenance
- **💧 Water Heaters** - Water heating system services

## 🔄 User Workflow

### For Customers:
1. **Browse Services** → View by category or see all services
2. **Select Service** → View detailed service information and pricing
3. **Request Service** → Login/Register (service is preserved) → Submit request with address and duration
4. **Track Requests** → View request history and costs in profile

### For Companies:
1. **Register Company** → Specify field of work or choose "All in One"
2. **Create Services** → Add services with descriptions and hourly rates
3. **Manage Requests** → View customer requests, revenue, and statistics
4. **Profile Management** → Showcase services and company information

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Django 3.1.14
- PostgreSQL (optional, SQLite works for development)

### Installation
1. **Clone the repository**
   ```bash
   git clone https://learn.zone01kisumu.ke/git/oragwelr/netfix.git
   cd netfix
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Open your browser and go to `http://localhost:8000`
   - Register as a customer or company to start using the platform

## 🧪 Testing

Run the test suite to ensure everything is working correctly:
```bash
python manage.py test
```

The application includes comprehensive tests for:
- User authentication and registration
- Service creation and management
- Service request functionality
- Profile management
- Navigation and routing

## 🌟 Key Features Highlights

- **🔄 Service Preservation**: Never lose your selected service during authentication
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **🎨 Modern UI**: Beautiful glass morphism design with cool blue theme
- **🔐 Secure Authentication**: Robust user management with proper access controls
- **📊 Analytics**: Companies can track requests, revenue, and customer statistics
- **🚀 Performance**: Optimized CSS with cache-busting for fast loading
- **♿ Accessibility**: Clean, readable interface with proper contrast and navigation

## 👨‍💻 Author

**Otieno Ragwel Rogers**
- GitHub: [@Oragwel](https://github.com/Oragwel)
- Email: tidings@outlok.com

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow Django best practices
- Maintain the existing code style and formatting
- Add tests for new features
- Update documentation as needed
- Ensure responsive design compatibility

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Copyright (c) 2025 Otieno Ragwel Rogers**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.

## 📞 Support

For support, email tidings@outlook.com or create an issue in the repository.

---

**NetFix** - Connecting customers with quality home service providers through modern technology. 🏠✨
