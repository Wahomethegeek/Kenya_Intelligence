from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import County
from .serializers import CountyListSerializer, CountyDetailSerializer

import anthropic
import json

@api_view(['GET'])
def county_list(request):
    """Return all 47 counties"""
    counties = County.objects.all()
    serializer = CountyListSerializer(counties, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def county_detail(request, slug):
    """Return a single county by slug"""
    try:
        county = County.objects.get(slug=slug)
    except County.DoesNotExist:
        return Response(
            {'error': 'County not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = CountyDetailSerializer(county)
    return Response(serializer.data)

@api_view(['GET'])
def county_compare(request):
    """Compare two counties by slug"""
    slug1 = request.query_params.get('county1')
    slug2 = request.query_params.get('county2')

    if not slug1 or not slug2:
        return Response(
            {'error': 'Provide county1 and county2 as query params'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        county1 = County.objects.get(slug=slug1)
        county2 = County.objects.get(slug=slug2)
    except County.DoesNotExist:
        return Response(
            {'error': 'One or both counties not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer1 = CountyDetailSerializer(county1)
    serializer2 = CountyDetailSerializer(county2)

    return Response({
        'county1': serializer1.data,
        'county2': serializer2.data
    })


def dashboard(request):
    """Render the dashboard template with Mapbox token"""
    context = {
        'mapbox_token': settings.MAPBOX_TOKEN
    }
    return render(request, 'dashboard.html', context)


@api_view(['POST'])
def county_ai_summary(request, slug):
    """Generate an AI summary for a county using Claude API"""
    try:
        county = County.objects.get(slug=slug)
    except County.DoesNotExist:
        return Response(
            {'error': 'County not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # A detailed prompt for the AI to generate a comprehensive summary of the county
    prompt = f"""
You are a Kenya county intelligence analyst. Generate a concise, 
insightful 3-sentence summary for {county.name} County based on 
this real data:

- Region: {county.region}
- Population: {county.population:,}
- Area: {county.area_km2} km²
- Hospitals: {county.hospitals}
- Health Centres: {county.health_centres}
- Primary Schools: {county.primary_schools}
- Secondary Schools: {county.secondary_schools}
- Poverty Index: {county.poverty_index}%
- Main Economic Activity: {county.main_activity}

Write a smart, data-driven summary that highlights what makes 
this county unique, its strengths, and key challenges.
Keep it under 80 words. Be specific, not generic.
    """

    client = anthropic.Client(api_key=settings.CLAUDE_API_KEY)
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=200,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    summary = message.content[0].text
    return Response({'summary': summary})