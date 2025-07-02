# Service Structure and Field Restrictions - NetFix

## Overview
NetFix implements a comprehensive service management system where companies are restricted to creating services only in their field of specialization, with the exception of "All in One" companies who can create services in any category.

## Service Structure
Every service in NetFix must include the following attributes:

### Required Service Attributes
1. **name** - The service name (e.g., "Emergency Plumbing Repair")
2. **description** - Detailed description of the service
3. **field** - Service category (must match available field options)
4. **price_hour** - Price per hour (decimal with 2 decimal places)
5. **date_created** - Automatically set when service is created (datetime)

## Company Field of Work Options
The following field of work options are available for companies:

1. **Air Conditioner**
2. **All in One** *(Special - can create services in any category)*
3. **Carpentry**
4. **Electricity**
5. **Gardening**
6. **Home Machines**
7. **Housekeeping**
8. **Interior Design**
9. **Locks**
10. **Painting**
11. **Plumbing**
12. **Water Heaters**

## Service Field Categories
Services can be categorized in the following fields (note: **NO "All in One" services allowed**):

1. **Air Conditioner**
2. **Carpentry**
3. **Electricity**
4. **Gardening**
5. **Home Machines**
6. **Housekeeping**
7. **Interior Design**
8. **Locks**
9. **Painting**
10. **Plumbing**
11. **Water Heaters**

## How It Works

### Specialized Companies
- A company with field of work "Plumbing" can **only** create services in the "Plumbing" category
- A company with field of work "Electricity" can **only** create services in the "Electricity" category
- And so on for all other specialized fields

### All in One Companies
- Companies with field of work "All in One" can create services in **any** category
- They can create Plumbing services, Electricity services, Painting services, etc.
- The only restriction is they cannot create services categorized as "All in One" (services must have specific categories)

## User Experience

### Service Creation Form
When a company tries to create a service:

1. **Company Info Banner** displays their specialization
2. **Field Dropdown** is automatically restricted to valid options:
   - Specialized companies see only their field
   - "All in One" companies see all fields except "All in One"
3. **Help Text** explains the restrictions
4. **Validation** prevents form submission with invalid fields

### Error Messages
If a company tries to create a service outside their specialization:
- Clear error message: "Your company specializes in 'Plumbing' services. You cannot create services in the 'Electricity' category."
- Suggestion to register as "All in One" company for broader service creation

## Examples

### Example 1: Plumbing Company
- **Company**: "PlumbingPro" (Field: Plumbing)
- **Can Create**: Plumbing services only
- **Cannot Create**: Electricity, Painting, or any other category services
- **Form Shows**: Only "Plumbing" option in field dropdown

### Example 2: All in One Company
- **Company**: "HomeServices" (Field: All in One)
- **Can Create**: Services in any category (Plumbing, Electricity, Painting, etc.)
- **Cannot Create**: Services categorized as "All in One"
- **Form Shows**: All field options except "All in One"

## Technical Implementation

### Database Level
- Service model validates field matches company's field of work
- Validation occurs on both form submission and direct model save

### Form Level
- Dynamic field choices based on company specialization
- Client-side prevention of invalid selections
- Server-side validation with clear error messages

### View Level
- Authentication checks ensure only companies can create services
- Company information passed to form for validation
- Proper error handling and user feedback

## Benefits

1. **Quality Control**: Ensures companies only offer services in their area of expertise
2. **User Trust**: Customers know they're getting specialized service providers
3. **Clear Expectations**: Companies understand their service creation limitations
4. **Flexibility**: "All in One" option allows versatile service providers
5. **Professional Standards**: Maintains service quality and specialization standards
