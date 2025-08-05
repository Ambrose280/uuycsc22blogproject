

inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host noprefixroute 
    inet 192.168.1.124/24 brd 192.168.1.255 scope global dynamic noprefixroute wlp0s20f3
    inet6 fe80::cfe6:5eb:dc9e:7383/64 scope link noprefixroute 
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
    inet 192.168.1.179/24 brd 192.168.1.255 scope global dynamic noprefixroute enx00a0c6000000
    inet6 fe80::211e:da51:8da5:ecb8/64 scope link noprefixroute 

    
````

This implementation:
1. Handles form submission
2. Validates required fields
3. Checks email format
4. Stores raw password in database (not recommended for production)
5. Handles duplicate username/email errors
6. Redirects to login page after successful registration

Make sure you have the templates directory created and the `signup.html` file in it before running the application.

**Note**: Storing plain text passwords is not secure and should never be done in a production environment. Always use password hashing in real applications.

Similar code found with 2 license types

Ambrose280: analyse the contentes of these files and gimme the basic desing of all the elements

GitHub Copilot: I'll analyze the template files and break down their basic design structure:

### Base Template (base.html)
- **Structure**:
  - Header with site title "My Blog"
  - Navigation bar with:
    - Home, About, Contact links
    - Conditional user menu (logged in/out state)
  - Main content area (`{% block content %}`)
  - Footer with copyright
- **Dynamic Elements**:
  - User welcome message if logged in
  - Login/Logout toggle
  - Create Post link for logged-in users

### Signup Page (signup.html)
- **Form Elements**:
  - Hidden CSRF token
  - Username input (text)
  - Email input (email)
  - Password input (password)
  - Submit button "Create Account"
- **Inherits base template**

### Login Page (login.html)
- **Form Elements**:
  - Hidden CSRF token
  - Username input
  - Password input
  - Login button
- **Additional Features**:
  - Error message display (in red)
  - Welcome message if logged in
- **Inherits base template**

### Create Post Page (createpost.html)
- **Form Elements**:
  - Hidden CSRF token
  - Title input
  - Featured image upload
  - Category dropdown
  - Draft checkbox
  - Content textarea (80 cols × 10 rows)
  - Submit button
- **Additional Features**:
  - Error message display
  - File upload support
- **Inherits base template**

### Edit Post Page (editpost.html)
- **Form Elements**:
  - Similar to create post but pre-filled
  - Current image display
  - Option to change image
  - Category selection (with current selection)
  - Draft status toggle
  - Content editor
  - Update button
- **Inherits base template**

### Add Category Page (add_category.html)
- **Form Elements**:
  - Hidden CSRF token
  - Category name input
  - Submit button
- **Additional Features**:
  - Error/success message display
- **Inherits base template**

### Post Detail Page (postdetail.html)
- **Display Elements**:
  - Post title
  - Timestamp
  - Reading time (if available)
  - Featured image (if available)
  - Post content
  - View count
- **Formatting**:
  - Pre-wrapped text formatting
  - Image sized to 600x400
- **Inherits base template**

### Common Design Patterns
1. All pages inherit from base.html
2. Consistent form structure
3. CSRF protection on all forms
4. Error handling displays
5. Responsive user feedback
6. Clear navigation hierarchy
7. User authentication awareness
8. File upload handling for images

This structure follows a clean, hierarchical template system with proper separation of concerns and consistent user interface elements across all pages.