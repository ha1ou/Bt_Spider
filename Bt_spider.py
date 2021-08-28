import requests,re,time,json
import threading,queue
import argparse,sys

que_list = queue.Queue()
def Get_Page_cid(start_page,end_page,head):
    url = "https://www.butian.net/Reward/pub"
    for page in range(start_page,end_page):
        data = {"s":1,
                "p":page,
                "token":""
            }
        res = requests.post(url,data=data,headers=head)
        json_data = json.loads(res.text) 
        data = json_data['data']['list'] 
        for i in range(len(data)):
            try:
                que_list.put(data[i]['company_id'])
            except:
                continue

def Get_Domain(head):
    site_list = []
    while not que_list.empty():
        cid = que_list.get()
        url  = 'https://www.butian.net/Loo/submit?cid=%s' % cid
        try:
            res = requests.get(url,headers=head)  
        except Exception as reason:
            continue
        try:
            site = re.findall('value="www\.(.*?)"',res.text)[0].strip().strip("/")
            if site not in site_list:
                print(site)
                domain_result.write("%s\n" % site)
                domain_result.flush()
                site_list.append(site)
            else:
                continue
            time.sleep(0.5)
        except Exception as reason:
            continue
            
def Thread_Start(thread_num,head):
    get_domain_thread_list = []

    for Get_domain_thread in range(thread_num):
        Get_domain_thread_1 = threading.Thread(target=Get_Domain,args=(head,))
        Get_domain_thread_1.start()
        get_domain_thread_list.append(Get_domain_thread_1)

    for domain_thread_join in get_domain_thread_list:
        domain_thread_join.join()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t",type=int,help="Thread Numbers(Default 5)",default=5)
    parser.add_argument("-s",type=int,help="Start Page(Default 1)",default=1)
    parser.add_argument("-e",type=int,help="End Page(Default 10)",default=10)
    parser.add_argument("-c",help="Login Cookie ")
    args = parser.parse_args()

    if args.c == None:
        print("\n[-]useage python3 bt.py --help")
        sys.exit()
        
    domain_result = open("domain_result.txt",'a',encoding="utf-8")
    head = {'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
                "Cookie": args.c
           }
    Get_Page_cid(args.s,args.e,head)
    Thread_Start(args.t,head)
    domain_result.close()
    
main()
