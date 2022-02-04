import nexity

if __name__ == '__main__':
    nexity.load_env()
    nexity.load_local('blurpo.ext.code')
    nexity.load_local('blurpo.ext.whitelist')
    nexity.run()
