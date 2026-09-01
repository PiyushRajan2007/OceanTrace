#!/usr/bin/env python
"""
End-to-end integration test script
Verifies that both frontend and backend are working together
"""
import sys
import urllib.request
import json
import time

def test_backend_health():
    """Test backend health endpoint"""
    try:
        resp = urllib.request.urlopen('http://127.0.0.1:8000/health')
        data = json.loads(resp.read())
        assert data['status'] == 'ok'
        print('✓ Backend health endpoint working')
        return True
    except Exception as e:
        print(f'✗ Backend health check failed: {e}')
        return False

def test_incident_endpoint():
    """Test incident data endpoint"""
    try:
        resp = urllib.request.urlopen('http://127.0.0.1:8000/api/v1/incidents/INC-240824-01')
        data = json.loads(resp.read())
        assert data['id'] == 'INC-240824-01'
        assert data['severity'] == 'Warning'
        print('✓ Incident endpoint working')
        return True
    except Exception as e:
        print(f'✗ Incident endpoint failed: {e}')
        return False

def test_vessels_endpoint():
    """Test vessels endpoint"""
    try:
        resp = urllib.request.urlopen('http://127.0.0.1:8000/api/v1/incidents/INC-240824-01/vessels')
        data = json.loads(resp.read())
        assert len(data) == 3
        assert data[0]['name'] == 'SEA ORCHID'
        print('✓ Vessels endpoint working')
        return True
    except Exception as e:
        print(f'✗ Vessels endpoint failed: {e}')
        return False

def test_frontend_ready():
    """Test frontend is accessible"""
    try:
        resp = urllib.request.urlopen('http://localhost:5173/')
        assert resp.status == 200
        print('✓ Frontend server running on http://localhost:5173')
        return True
    except Exception as e:
        print(f'✗ Frontend not yet ready: {e}')
        return False

def main():
    print('=' * 60)
    print('OCEANTRACE END-TO-END INTEGRATION TEST')
    print('=' * 60)
    print()
    
    print('Backend Tests:')
    print('-' * 60)
    backend_ok = test_backend_health()
    backend_ok &= test_incident_endpoint()
    backend_ok &= test_vessels_endpoint()
    print()
    
    print('Frontend Tests:')
    print('-' * 60)
    frontend_ok = test_frontend_ready()
    print()
    
    if backend_ok and frontend_ok:
        print('✓ ALL TESTS PASSED')
        print()
        print('Access the dashboard at: http://localhost:5173/')
        print('Backend API at: http://127.0.0.1:8000/')
        print('Swagger docs at: http://127.0.0.1:8000/docs')
        print()
        return 0
    else:
        print('✗ SOME TESTS FAILED')
        if not backend_ok:
            print('  - Backend issues detected')
        if not frontend_ok:
            print('  - Frontend issues detected')
        return 1

if __name__ == '__main__':
    sys.exit(main())
