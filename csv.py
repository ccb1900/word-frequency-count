import redis as rds
pool = rds.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = rds.Redis(connection_pool=pool)
def generate_file(r,name):
    results = r.zrevrange(name,0,-1,True)
    f = open(name+".csv","wb")

    for x in results:
        f.write((x[0] + ',' + str(int(x[1])) + "\n").encode("UTF-8"))
    f.close()

generate_file(r,"words-lower")
generate_file(r,"words-upper")
generate_file(r,"words-title")