from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from home.models import SmileCenter
from home.models import CenterType
from home.models import SmileCenterByCenterType
from rest_framework import viewsets, filters
from .models import SmileCenter
from .serializers import SmileCenterSerializer
from .models import SmileCenterByServices
from .models import Zone
from .models import SmileCenterByZones
from .models import Service
from rest_framework import generics
from .serializers import ZoneSerializer
from rest_framework.filters import SearchFilter
from .serializers import ServiceSerializer
from .serializers import CenterTypeSerializer
from drf_yasg.utils import swagger_auto_schema

#------View for the requests of SmileCenters
class SmileCenterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SmileCenter.objects.all()
    serializer_class = SmileCenterSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['zone','center_type_name']

    def get_queryset(self):
        queryset = SmileCenter.objects.all()

        # Filter by zone if provided
        zone = self.request.query_params.get('zone', None)
        if zone:
            queryset = queryset.filter(zone=zone)

        # Filter by center_type_name if provided
        center_type_name = self.request.query_params.get('center_type_name', None)
        if center_type_name:
            queryset = queryset.filter(center_type_name=center_type_name)

        # Filter by product_id from Service model
        product_id = self.request.query_params.get('product_id', None)
        if product_id:
            try:
                service = Service.objects.get(product_id=product_id)
                smile_centers_ids = SmileCenterByServices.objects.filter(services_id=service.id).values_list('smile_center_id', flat=True)
                queryset = queryset.filter(id__in=smile_centers_ids)
            except Service.DoesNotExist:
                queryset = queryset.none()

        return queryset

#-------View for the requests of Zones
class ZoneListView(generics.ListAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    filter_backends = [SearchFilter]
    search_fields = ['zone']

    @swagger_auto_schema(operation_description="Retrieve a list of Zones",
                         responses={200: ZoneSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

#-------View for the requests of Services

class ServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        queryset = Service.objects.all()
        product_id = self.request.query_params.get('product_id', None)
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset
    
    @swagger_auto_schema(operation_description="Retrieve a list of Services",
                         responses={200: ServiceSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

#-------View for request for Center Type
class CenterTypeListView(generics.ListAPIView):
    serializer_class = CenterTypeSerializer


    def get_queryset(self):
        queryset = CenterType.objects.all()
        center_type_name = self.request.query_params.get('center_type_name', None)
        if center_type_name is not None:
            queryset = queryset.filter(center_type_name__icontains=center_type_name)
        return queryset
    
    @swagger_auto_schema(operation_description="Retrieve a list of center types",
                         responses={200: CenterTypeSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


url = 'https://parseapi.back4app.com/classes/SmileCenters/'

headers = {
    "X-Parse-Application-Id": "7mLDGFkL3dPCHu9Z4kJNkdQWgflCvRVBngfRb3OJ",
 "X-Parse-REST-API-Key": "tlmsEFP2dkilRzLhQCbW6lgmaO3O0Lig6xodNoFt"
}

where_clause = {
        #"Center_Type": "Centro Aliado"
    }

params = {
    "where": json.dumps(where_clause)
}



#This line adds a cache to the view, preventing requests that can overload the service. It's updated every 15 mins
@cache_page(60 * 15)
def users(request):
    #pull data from third party rest api
    response = requests.get(url, headers=headers, params=params)

    #convert reponse data into json
    users = response.json()

    #Sending the data to the function we are sorting
    insertDataSmileCenter(users)

    #print(users)
    return render(request, "users.html", {'users': users})

    pass



def insertDataSmileCenter(json_data):
#-------Inserting Center Types
    data = json_data
    center_types = set()  # Using a set to store distinct center names
    
    # Extract Center_Name values and add to the set
    for item in data.get("results", []):
        center_type = item.get("Center_Type")
        if center_type:
            center_types.add(center_type)
    
        # Process CenterType
        center_type_name = item.get("Center_Type", "")
        if center_type_name:
            center_type, created = CenterType.objects.get_or_create(
                center_type_name=center_type_name
            )

#-------Inserting Zones
    data = json_data
    zones = set() 
    # Extract Zone values and add to the set
    for item in data.get("results", []):
        zone = item.get("Zone")
        if zone:
            zones.add(zone)
    
        # Process CenterType
        zone = item.get("Zone", "")
        if zone:
            zone, created = Zone.objects.get_or_create(
                zone=zone
            )

#-------Inserting Services


    results = json_data['results']

    # Iterate over each item in the 'results' list
    for item in results:
        if not isinstance(item, dict):
            print(f"Invalid item format: {item}")
            continue
        
        services_str = item.get("Services")
        
        try:
            services = json.loads(services_str) if isinstance(services_str, str) else services_str
        except json.JSONDecodeError:
            print(f"Invalid services JSON for ID: {item.get('ID')}")
            continue

        if not isinstance(services, dict):
            print(f"Invalid services format for ID: {item.get('ID')}")
            continue
        
        for service_name, service_data in services.items():
            if not isinstance(service_data, dict):
                print(f"Invalid service data format for {service_name}: {service_data}")
                continue
            
            product_id = service_data.get("productId")
            appointment_type_id = service_data.get("AppointmentTypeId")
            
            if product_id and appointment_type_id:
                service, created = Service.objects.get_or_create(
                    product_id=product_id,
                    defaults={'appointment_type_id': appointment_type_id}
                )

                
                if not created:
                    service.appointment_type_id = appointment_type_id
                    service.save()
   
            
            else:
                print(f"Invalid service data for {service_name}: {service_data}")

#-------Inserting SmileCenters
    for item in json_data.get("results", []):
        center_id = item.get("ID")
        
        if not center_id:
            continue
        
        # Check if the center with the given ID already exists
        center, created = SmileCenter.objects.get_or_create(id_external=center_id)

        
        # Update the fields
        center.number = item.get("Number")
        center.city = item.get("City")
        center.neighborhood = item.get("Neighborhood")
        center.state = item.get("State")
        center.apt = item.get("Apt")
        center.region = item.get("Region")
        center.name = item.get("Center_Name")
        center.time_table = item.get("Timetable")
        center.cp = item.get("Zip")
        center.street = item.get("Street")
        center.country = item.get("Country")
        center.center_type_name = item.get("Center_Type")
        center.services = item.get("Services")
        center.zone = item.get("Zone")

        center.save()

#--------Inserting in SmileCenterByService

    results = json_data['results']

    # Iterate over each item in the 'results' list
    for item in results:
        if not isinstance(item, dict):
            print(f"Invalid item format: {item}")
            continue

        services_str = item.get("Services")

        try:
            services = json.loads(services_str) if isinstance(services_str, str) else services_str
        except json.JSONDecodeError:
            print(f"Invalid services JSON for ID: {item.get('ID')}")
            continue

        if not isinstance(services, dict):
            print(f"Invalid services format for ID: {item.get('ID')}")
            continue

        for service_name, service_data in services.items():
            if not isinstance(service_data, dict):
                print(f"Invalid service data format for {service_name}: {service_data}")
                continue

            product_id = service_data.get("productId")
            
            if product_id:
                try:
                    service = Service.objects.get(product_id=product_id)
                    service_id = service.id
                    # Insert into SmileCenterByServices
                    SmileCenterByServices.objects.get_or_create(
                        smile_center_id=consultSmileCenterID(item.get("ID")),
                        services_id=service_id
                    )
                except Service.DoesNotExist:
                    print(f"Service with product_id {product_id} does not exist")
            else:
                print(f"Invalid service data for {service_name}: {service_data}")


#--------Inserting in model SmileCenterByCenterType
    for item in json_data.get("results", []):
        center_id = item.get("ID") 

        SmileCenterByCenterType.objects.get_or_create(
        smile_center_id=consultSmileCenterID(item.get("ID")),
        center_type_id=consultCenterTypeID(item.get("Center_Type")))



#--------Inserting in model SmileCenterByZone
    for item in json_data.get("results", []):
        center_id = item.get("ID") 

        SmileCenterByZones.objects.get_or_create(
        smile_center_id=consultSmileCenterID(item.get("ID")),
        zone_id=consultZoneID(item.get("Zone")))


    return








#Function that obtains ID from CenterType
def consultCenterTypeID(center_type_name):
    try:
        center_type = CenterType.objects.get(center_type_name=center_type_name)
        return center_type.id
    except CenterType.DoesNotExist:
        return None

#Function that obtains ID from SmileCenter searching by Id external
def consultSmileCenterID(id_external):
    try:
        smilecenter = SmileCenter.objects.get(id_external=id_external)
        return smilecenter.id
    except CenterType.DoesNotExist:
        return None

#Function that obtains ID from Service searching by product_id
def consultServiceID(product_id):
    try:
        service = Service.objects.get(product_id=product_id)
        return service.id
    except Service.DoesNotExist:
        return None

#Function that obtains ID from Service searching by product_id
def consultZoneID(zone):
    try:
        zone = Zone.objects.get(zone=zone)
        return zone.id
    except Zone.DoesNotExist:
        return None




def sortDatabyZone(data):

    zones = set()
    results = data.get('results', [])

    for entry in results:
        if "Zone" in entry:
            zones.add(entry["Zone"])

    return list(zones)





