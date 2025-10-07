import json 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from .models import Repository, Build

@csrf_exempt 
def github_webhook(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            repo_name = payload['repository']['name']
            repo_url = payload['repository']['html_url']
            commit_id = payload['after']

            repo, _ = Repository.objects.get_or_create(name=repo_name, repo_url=repo_url)
            build = Build.objects.create(repository=repo, commit_id=commit_id, status='pending')

            #For now, we'll simulate a simple build
            build.status = 'running'
            build.log = "Build started.. \n"
            build.save()

            #later we'll replace this with actual commands
            build.log += 'Simulating build.. \nBuild successful'
            build.status = 'success'
            build.save()

            return JsonResponse({'message': 'Build triggered successfully'}, status=200)

        except Exception as e:
            print(e)
            return JsonResponse({'error':str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)
