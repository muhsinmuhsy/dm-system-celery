from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import whois
from .utils import format_dates, ensure_list
from django.contrib.auth.decorators import login_required
from .models import Domain, ExpirationDate, UpdatedDate, CreationDate, Email
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from auth_app.models import User
from .tasks import send_mail_func, check_expiring_domains
from django.http.response import HttpResponse

def home(request):
    whois_domain = None
    no_data_message = None
    current_page = 'home'
    if request.method == 'POST':
        domain = request.POST.get('domain')

        try:
            whois_data = whois.whois(domain)
            updated_date_str = format_dates(ensure_list(whois_data.updated_date))
            creation_date_str = format_dates(ensure_list(whois_data.creation_date))
            expiration_date_str = format_dates(ensure_list(whois_data.expiration_date))
            
            # Ensure all necessary fields are lists
            domain_name = whois_data.domain_name
            if isinstance(domain_name, list):
                domain_name = domain_name[0]

            whois_domain = {
                "domain_name": domain_name,
                "registrar": ensure_list(whois_data.registrar),
                "whois_server": ensure_list(whois_data.whois_server),
                "referral_url": ensure_list(whois_data.referral_url),
                "updated_date": updated_date_str,
                "creation_date": creation_date_str,
                "expiration_date": expiration_date_str,
                "name_servers": ensure_list(whois_data.name_servers),
                "status": ensure_list(whois_data.status),
                "emails": ensure_list(whois_data.emails),
                "dnssec": ensure_list(whois_data.dnssec),
                "name": ensure_list(whois_data.name),
                "org": ensure_list(whois_data.org),
                "address": ensure_list(whois_data.address),
                "city": ensure_list(whois_data.city),
                "state": ensure_list(whois_data.state),
                "registrant_postal_code": ensure_list(whois_data.registrant_postal_code),
                "country": ensure_list(whois_data.country),
            }

            if not whois_domain['domain_name']:
                no_data_message = 'No data found for the domain'
            
        except Exception as e:
            no_data_message = 'No data found for the domain'
            # messages.error(request, f'Error: {str(e)}')
            
    context = {
        'whois_domain': whois_domain,
        'no_data_message': no_data_message,
        'current_page' : current_page
    }
    return render(request, 'customer_app/home.html', context)

@login_required(login_url='customer_signin')
def save_domain(request):
    whois_data = None
    referer_url = request.META.get('HTTP_REFERER', 'home')  # Default to 'home' if no referer URL is present

    if request.method == 'POST':
        domain = request.POST.get('domain')
        user = request.user
        
        if not domain:
            messages.error(request, 'Domain name is required.')
            return redirect(referer_url)

        try:
            whois_data = whois.whois(domain)
            
            if not whois_data['domain_name']:
                messages.error(request, 'No data found for the Domain')
                return redirect(referer_url)
            
            domain_name = whois_data.domain_name
            if isinstance(domain_name, list):
                domain_name = domain_name[0]
            
            # Check if the domain is already saved for the user
            if Domain.objects.filter(user=user, domain_name=domain_name).exists():
                messages.error(request, 'Domain is already saved.')
                return redirect(referer_url)
            
            # Fetch Whois data
            
            updated_dates = ensure_list(whois_data.updated_date) if whois_data.updated_date else []
            creation_dates = ensure_list(whois_data.creation_date) if whois_data.creation_date else []
            expiration_dates = ensure_list(whois_data.expiration_date) if whois_data.expiration_date else []
            emails = ensure_list(whois_data.emails) if whois_data.emails else []

            # Create the Domain object
            domain = Domain.objects.create(
                user=user,
                domain_name=domain_name,
                registrar=whois_data.registrar,
                whois_server=whois_data.whois_server,
                referral_url=whois_data.referral_url,
                name_servers=whois_data.name_servers,
                status=whois_data.status,
                dnssec=whois_data.dnssec,
                name=whois_data.name,
                org=whois_data.org,
                address=whois_data.address,
                city=whois_data.city,
                state=whois_data.state,
                registrant_postal_code=whois_data.registrant_postal_code,
                country=whois_data.country,
            )
            
            # Create and associate Expiration Date objects
            for expiration_date in expiration_dates:
                ExpirationDate.objects.create(domain=domain, expiration_date=expiration_date)
                
            # Create and associate Updated Date objects
            for updated_date in updated_dates:
                UpdatedDate.objects.create(domain=domain, updated_date=updated_date)
                
            # Create and associate Creation Date objects
            for creation_date in creation_dates:
                CreationDate.objects.create(domain=domain, creation_date=creation_date)
                
            # Create and associate Email objects
            for email in emails:
                Email.objects.create(domain=domain, emails=email)
            
            messages.success(request, 'Domain saved successfully.')
        except Exception as e:
            messages.error(request, 'No Data Found')
            # messages.error(request, f'Unexpected error: {str(e)}')

    return redirect(referer_url)
    

# @login_required(login_url='customer_signin')
# def user_domains(request):
#     user = request.user
#     domains = Domain.objects.filter(user=user)
#     return render(request, 'customer_app/user_domains.html', {'domains': domains})

# @login_required(login_url='customer_signin')
# def user_domains(request):
#     user = request.user
#     query = request.GET.get('q', '')  # Default to empty string if no query is provided
#     if query:
#         domains = Domain.objects.filter(user=user, domain_name__icontains=query)
#     else:
#         domains = Domain.objects.filter(user=user)
#     return render(request, 'customer_app/user_domains.html', {'domains': domains, 'query': query})

@login_required(login_url='customer_signin')
def user_domains(request):
    user = request.user
    count = Domain.objects.filter(user=user).count()
    query = request.GET.get('q', '') 
    if query:
        domains = Domain.objects.filter(user=user, domain_name__icontains=query)
    else:
        domains = Domain.objects.filter(user=user)

    paginator = Paginator(domains, 10)  
    page = request.GET.get('page')
    try:
        domains = paginator.page(page)
    except PageNotAnInteger:
        domains = paginator.page(1)
    except EmptyPage:
        domains = paginator.page(paginator.num_pages)

    return render(request, 'customer_app/user_domains.html', {'domains': domains, 'query': query, 'count': count})


@login_required(login_url='customer_signin')
def refresh_domain(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id, user=request.user)

    try:
        # Fetch new Whois data
        whois_data = whois.whois(domain.domain_name)
        updated_dates = ensure_list(whois_data.updated_date) if whois_data.updated_date else []
        creation_dates = ensure_list(whois_data.creation_date) if whois_data.creation_date else []
        expiration_dates = ensure_list(whois_data.expiration_date) if whois_data.expiration_date else []
        emails = ensure_list(whois_data.domain) if whois_data.domain else []

        # Delete existing related data
        domain.updated_dates.all().delete()
        domain.creation_dates.all().delete()
        domain.expiration_dates.all().delete()
        domain.emails.all().delete()

        # Update Domain object
        domain.registrar = whois_data.registrar
        domain.whois_server = whois_data.whois_server
        domain.referral_url = whois_data.referral_url
        domain.name_servers = whois_data.name_servers
        domain.status = whois_data.status
        domain.dnssec = whois_data.dnssec
        domain.name = whois_data.name
        domain.org = whois_data.org
        domain.address = whois_data.address
        domain.city = whois_data.city
        domain.state = whois_data.state
        domain.registrant_postal_code = whois_data.registrant_postal_code
        domain.country = whois_data.country
        domain.save()

        # Create new related data
        for updated_date in updated_dates:
            UpdatedDate.objects.create(domain=domain, updated_date=updated_date)

        for creation_date in creation_dates:
            CreationDate.objects.create(domain=domain, creation_date=creation_date)

        for expiration_date in expiration_dates:
            ExpirationDate.objects.create(domain=domain, expiration_date=expiration_date)

        for email in emails:
            Email.objects.create(domain=domain, emails=email)

        messages.success(request, 'Domain updated successfully.')
    except Exception as e:
        messages.error(request, f'Error refreshing domain: {str(e)}')

    return redirect('user_domains')

   

@login_required(login_url='customer_signin')
def delete_domain(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id, user=request.user)

    try:
        domain.delete()

        messages.success(request, 'Domain deleted successfully.')
    except Exception as e:
        messages.error(request, f'Error deleting domain: {str(e)}')

    return redirect('user_domains')

def profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'customer_app/profile.html', context)



@login_required
def edit_profile(request):
    user = request.user
    User = get_user_model()  # Get the user model
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        # Validate email
        try:
            if email:
                validate_email(email)
                
                # Check if the email is already taken by another user
                if User.objects.filter(email=email).exclude(id=user.id).exists():
                    messages.error(request, 'This email address is already in use.')
                    return render(request, 'edit_profile.html', {'user': user})
        except ValidationError:
            messages.error(request, 'Invalid email address.')
            return render(request, 'edit_profile.html', {'user': user})

        # Update user profile
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        
        user.save()
        messages.success(request, 'Your profile was updated successfully!')
        return redirect('profile')  

    return render(request, 'customer_app/edit_profile.html', {'user': user})



@login_required(login_url='customer_signin')
def doamin_details(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id)
    context = {
        'domain' : domain
    }
    return render(request, 'customer_app/doamin_details.html', context)

@login_required(login_url='customer_signin')
def settings(request):
    return render(request, 'customer_app/settings.html')

@login_required(login_url='customer_signin')
def notification(request):
    user = request.user
    user_ntfy = User.objects.filter(id=user.id)
    
    if request.method == 'POST':
        notification_preference = request.POST.get('notification_preference')
        try:
            user_ntfy.update(
                notification_preference = notification_preference
            )
            messages.success(request, 'Changed Successfully')
            return redirect('notification')
        
        except ValueError:
            messages.error(request, 'Please select a day')
            return redirect('notification')
        except Exception as e:
            messages.error(request, 'Error Failed to change')
            print(f'Error: {str(e)}')
            return redirect('notification')
    
    context = {
        'user' : user
    }
    return render(request, 'customer_app/notification.html', context)


def send_mail(request):
    send_mail_func.delay()
    return HttpResponse("Sent")

def check_expiring(request):
    check_expiring_domains.delay()
    return HttpResponse("Sent")
    