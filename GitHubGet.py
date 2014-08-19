# download an entire github repo.
#
# either copy the url to clipboard, and run script, or run following bookmarklet.  
# will unzip to repo-branch (so be careful if downloading same branch name from multiple users)
# 
##   javascript:(function()%7Bif(document.location.href.indexOf('http')===0)document.location.href='pythonista://GitHubGet?action=run&argv='+document.location.href;%7D)();

import clipboard, functools, os, re, sys, tempfile, urllib, zipfile

def extract_git_id(git):
    print('extract_git_id({})'.format(git)),
    return re.match((r'^http(s?)://([\w-]*\.)?github\.com/(?P<user>[\w-]+)/(?P<repo>[\w-]*)'
                 '((/tree|/blob)/(?P<branch>[\w-]*))?'), git)
    
def git_download_from_args(args):
    url = args[0] if args else clipboard.get()
    git_download(url)

def dlProgress(filename, count, blockSize, totalSize):
    percent = 100 if count*blockSize > totalSize else max(min(int(count*blockSize*100/totalSize),100),0)
    sys.stdout.write("\r" + filename + "...%d%%" % percent)
    sys.stdout.flush()

def git_download(url):
    m=extract_git_id(url)
    if not m:
        print('could not determine repo url from ' + url)
        return
    g=m.groupdict()
    g['branch'] = g['branch'] or 'master'
    url = 'https://codeload.github.com/{user}/{repo}/zip/{branch}'.format(**g)
    try:
        with tempfile.NamedTemporaryFile(mode='w+b',suffix='.zip') as f:
            urllib.urlretrieve(url,f.name,reporthook=functools.partial(dlProgress,url))
            z=zipfile.ZipFile(f)
            z.extractall()
            print('\n{}\n'.format('\n'.join(z.namelist())))
    except Exception as e:
        print('git url did not return zip file\n{}: {}'.format(type(e), e))
        
if __name__=='__main__':
    git_download_from_args(sys.argv[1:])
