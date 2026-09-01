import urllib.request
import json
import re
import os

def fetch_github_data(username):
    headers = {'User-Agent': 'Mozilla/5.0'}
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    # User info
    user_url = f'https://api.github.com/users/{username}'
    public_repos = 1
    followers = 3
    try:
        req = urllib.request.Request(user_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            public_repos = data.get('public_repos', 1)
            followers = data.get('followers', 3)
    except Exception as e:
        print('User API error:', e)
        
    # Repos info
    repos_url = f'https://api.github.com/users/{username}/repos?per_page=100'
    total_stars = 0
    lang_bytes = {}
    try:
        req = urllib.request.Request(repos_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            repos = json.loads(resp.read().decode())
            for r in repos:
                total_stars += r.get('stargazers_count', 0)
                l_url = r.get('languages_url')
                if l_url:
                    try:
                        l_req = urllib.request.Request(l_url, headers=headers)
                        with urllib.request.urlopen(l_req, timeout=5) as l_resp:
                            l_data = json.loads(l_resp.read().decode())
                            for lang, b in l_data.items():
                                lang_bytes[lang] = lang_bytes.get(lang, 0) + b
                    except:
                        pass
    except Exception as e:
        print('Repos API error:', e)
        
    return {
        'public_repos': public_repos,
        'followers': followers,
        'total_stars': total_stars,
        'lang_bytes': lang_bytes
    }

def update_stats_svg(stats_file, data):
    if not os.path.exists(stats_file):
        return
    with open(stats_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace stars, repos, followers values
    content = re.sub(r'(Total Stars Earned:.*?fill="#f59e0b">)\d+\+?(</text>)', rf'\g<1>{data["total_stars"]}\2', content)
    content = re.sub(r'(Public Repos:.*?fill="#22d65e">)\d+\+?(</text>)', rf'\g<1>{data["public_repos"]}\2', content)
    content = re.sub(r'(Followers:.*?fill="#3b82f6">)\d+\+?(</text>)', rf'\g<1>{data["followers"]}\2', content)
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {stats_file}')

def update_trophies_svg(trophies_file, data):
    if not os.path.exists(trophies_file):
        return
    with open(trophies_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = re.sub(r'(Stargazer.*?Stars )\d+', rf'\g<1>{data["total_stars"]}', content, flags=re.DOTALL)
    content = re.sub(r'(Creator.*?Repos )\d+', rf'\g<1>{data["public_repos"]}', content, flags=re.DOTALL)
    
    with open(trophies_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {trophies_file}')

if __name__ == '__main__':
    username = 'Salava-marquina'
    data = fetch_github_data(username)
    print('Fetched GitHub Data:', data)
    
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    update_stats_svg(os.path.join(root_dir, 'Salava-marquina-stats.svg'), data)
    update_trophies_svg(os.path.join(root_dir, 'Salava-marquina-trophies.svg'), data)
