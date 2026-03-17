from rest_framework import viewsets, response, decorators
from business_partner.models import Shop, SiteConfigs
from accounts.serializers import UserSerializer
from business_partner.serializers import ShopSerializer, SiteConfigsSerializer
from business_partner.utils import extract_domain

class SiteConfigsViewSet(viewsets.ModelViewSet):
    queryset = SiteConfigs.objects.all()
    serializer_class = SiteConfigsSerializer

    @decorators.action(detail=False, methods=['get'])
    def site_configs(self, request, *args, **kwargs):
        """
        Get the shop's site configs
        """
        try:
            domain = extract_domain(request)
            site_config = self.queryset.filter(shop__domain=domain).first()
            if site_config:
                serialized_data = SiteConfigsSerializer(site_config).data
                return response.Response({"data": serialized_data}, status=200)
            else:
                return response.Response({"error": "Site configurations not found"}, status=404)
        except Exception:
            return response.Response({"error": "An error occurred while fetching site configurations"}, status=500)

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    @decorators.action(detail=False, methods=['post'])
    def onboard_new_partner(self, request, *args, **kwargs):
        """
        Custom action to onboard a new business partner.
        This could include creating default site configurations or other setup tasks.
        """
        shop_details = request.data.get('shop_details',{})
        owner_details = request.data.get('owner_details',{})
        shop_data = {
            'name': shop_details.get('business_name',''),
            'url': shop_details.get('url',''),
            'domain': shop_details.get('domain','')
        }
        try:
            shop_data = ShopSerializer(data=shop_data)
            if shop_data.is_valid(raise_exception=True):
                shop = shop_data.save()
                owner_details['shop'] = shop.id
                # Create default site configurations
                #TODO: create function to send media to object storage 
                site_configs_details = {
                    'shop': shop.id,
                    'color_palette': shop_details.get('color_palette', "#E65A3D"),
                    'logo_url': shop_details.get('logo_url', None),
                    'hero_image_url': shop_details.get('hero_image_url', None),
                    'hero_text': shop_details.get('hero_text', '')
                }
                site_configs_data = SiteConfigsSerializer(data=site_configs_details)
                if site_configs_data.is_valid(raise_exception=True):
                    site_configs_data.save()

            owner_data = UserSerializer(data=owner_details)
            if owner_data.is_valid():
                owner_data.save()

            return response.Response({"status": "Business partner onboarded successfully"}, status=201)
        except Exception as e:
            return response.Response({"error": str(e)})
