from business_partner.models import Shop

def extract_domain(request):
    domain = request.get_host()
    if not domain:
        return None
    deconstructed_domain= domain.split('.')
    if len(deconstructed_domain) == 2:
        subdomain = deconstructed_domain[0]
        return subdomain
    return domain

def get_shop(request):
    domain = extract_domain(request)
    shop = Shop.objects.filter(domain=domain).first()
    if shop:
        return shop
    # revert to "admin shop"
    # TODO: Fix this bs tho
    return Shop.objects.filter(domain='mirror_moodz').first()