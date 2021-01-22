import argparse
import sys
import json
import logging
import pandas

from NCentralClient import NCentralClient, NCentralError

def main():
    """Main function"""
    parser = argparse.ArgumentParser(prog='pyncentral')
    parser.add_argument('-username', required=True, help='NCentral username')
    parser.add_argument('-password', required=True, help='NCentral Password')
    parser.add_argument('-url', required=True, help='NCentral base url')
    parser.add_argument('-debug', action='store_true', help='Print debug messages to stderr')

    subparsers = parser.add_subparsers(dest='type')

    #All Customers
    parser_customer_all = subparsers.add_parser('all', help="Global actions that don't need a cutomer id")
    parser_customer_all.add_argument('all_customer_action', type=str,default='list', help='List Customers', choices=['list'])
    parser_customer_all.add_argument('--filter', required=False, type=str, help='Enter search term')

    #Spesific CustomerID
    parser_customerid = subparsers.add_parser('customer', help='Customer related actions')
    parser_customerid.add_argument('--customerid', required=True, type=int, help='Enter customer id')
    parser_customerid.add_argument('--filter', required=False, type=str, help='Enter search term')

    #Spesific CustomerID related functions
    subparsers_customerid_action = parser_customerid.add_subparsers(dest='customerid_action')
    parser_customerid_action = subparsers_customerid_action.add_parser('list', help='List devices under customer')
    parser_customerid_action = subparsers_customerid_action.add_parser('activeissue', help='List active issues under customer')

    #Device related functions
    parser_deviceid = subparsers.add_parser('device', help='device related actions')
    parser_deviceid.add_argument('--deviceid', required=True, type=int, help='Enter device id')
    parser_deviceid.add_argument('--filter', required=False, type=str, help='Enter search term')

    #DeviceID related functions
    subparsers_deviceid_action = parser_deviceid.add_subparsers(dest='deviceid_action')
    parser_deviceid_action = subparsers_deviceid_action.add_parser('list', help='List tasks under device')
    parser_deviceid_action = subparsers_deviceid_action.add_parser('deviceinfo', help='Get device info')
    
    #Task related functions
    parser_taskid = subparsers.add_parser('task', help='task related actions')
    parser_taskid.add_argument('--taskid', required=True, type=int, help='Enter task id')

    #TaskID related functions
    subparsers_taskid_action = parser_taskid.add_subparsers(dest='taskid_action')
#    parser_taskid_action = subparsers_taskid_action.add_parser('list', help='List tasks under customer')
    parser_taskid_action = subparsers_taskid_action.add_parser('pause', help='Pause task under customer')
    parser_taskid_action = subparsers_taskid_action.add_parser('resume', help='Resume task under customer')



    args = parser.parse_args()

    print(args)

    client = NCentralClient(args.username, args.password, args.url)


    if args.debug:

        import http.client
        http.client.HTTPConnection.debuglevel = 5
        # You must initialize logging, otherwise you'll not see debug output.
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True


    if args.type == 'all':

        if args.all_customer_action == 'list':
            if not args.filter:
                print(json.dumps(client.customerList(), indent=2))
            if args.filter:
                print(json.dumps(client.customerList(args.filter), indent=2))
        quit()

    if args.type == 'customer':

        if args.customerid_action == 'list':
            if not args.filter:
                print(json.dumps(client.deviceList(args.customerid), indent=2))
            if args.filter:
                print(json.dumps(client.deviceList(args.customerid, args.filter), indent=2))

        if args.customerid_action == 'activeissue':
            if not args.filter:
                print(json.dumps(client.activeissueslist(args.customerid), indent=2))
            if args.filter:
                print(json.dumps(client.activeissueslist(args.customerid, args.filter), indent=2))

        quit()

    if args.type == 'device':

        if args.deviceid_action == 'list':
            if not args.filter:
                print(json.dumps(client.deviceGetStatus(args.deviceid), indent=2))
            if args.filter:
                print(json.dumps(client.deviceGetStatus(args.deviceid, args.filter), indent=2))

        if args.deviceid_action == 'deviceinfo':
            if not args.filter:
                print(json.dumps(client.deviceGet(args.deviceid), indent=2))
            if args.filter:
                print(json.dumps(client.deviceGet(args.deviceid, args.filter), indent=2))

        quit()

    if args.type == 'task':

        if args.taskid:
            if args.taskid_action == 'pause':
                print(client.taskPauseMonitoring(args.taskid))

            if args.taskid_action == 'resume':
                print(client.taskResumeMonitoring(args.taskid))

#        if not args.taskid:
            if not args.taskid_action:
                print("not implemented, please use pause or resume")

        quit()

    else:
        print("Action not implemented: %s", args)

if __name__ == '__main__':
    sys.exit(main())