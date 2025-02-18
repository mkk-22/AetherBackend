from django.shortcuts import render, redirect
from devices.models import Device
from devicesharing.models import Listing, Request
from django.contrib.auth.decorators import login_required

@login_required
def ds_main(request):
    owner = request.user.owner
    my_listings = Listing.objects.filter(owner=owner)
    pending_requests = Request.objects.filter(listing__owner=owner, status='pending')
    active_requests = Request.objects.filter(listing__owner=owner, status='active')
    return render(request, 'ds_main.html', {'my_listings':my_listings, 'pending_requests':pending_requests, 'active_requests':active_requests})

@login_required
def add_listing(request):
    owner = request.user.owner  
    devices = Device.objects.filter(room__house__owner=owner, general_product_code__startswith='S')  
    if request.method == 'POST':
        device_id = request.POST.get('device_id', '').strip()
        device = Device.objects.filter(device_id=device_id).first()
        condition = request.POST.get('condition', '').strip()
        if device:
            Listing.objects.create(owner=owner, device=device, condition=condition)
        return redirect('ds_main')
    return render(request, 'add_listing.html', {'devices': devices})

@login_required
def remove_listing(request, device_id):
    owner = request.user.owner
    listing = Listing.objects.filter(owner=owner, device__device_id=device_id).first()
    listing.delete()
    return redirect('ds_main')

@login_required
def approve_request(request, req_id):
    req = Request.objects.filter(id=req_id).first()
    if req:
        req.status = 'active'  
        req.save()
        listing = req.listing
        listing.has_requested = True  
        listing.save()  
    return redirect('ds_main')

@login_required
def decline_request(request, req_id):
    req = Request.objects.filter(id=req_id)
    req.delete()
    return redirect('ds_main')   

@login_required
def search_results(request):
    query = request.GET.get('query', '').strip()
    listings = Listing.objects.filter(device__general_product_code__icontains=query)
    listings = listings.exclude(owner=request.user.owner)
    listings = listings.exclude(request__user=request.user.owner, request__status='active')
    for listing in listings:
        listing.has_requested = Request.objects.filter(listing=listing, user=request.user.owner).exists()
    return render(request, 'search.html', {'listings': listings})

@login_required
def create_request(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    existing_request = Request.objects.filter(listing=listing, user=request.user.owner)
    if not existing_request.exists():
        Request.objects.create(listing=listing, user=request.user.owner, status='pending')
    return redirect('search_results')  