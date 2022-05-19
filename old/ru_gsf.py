from RU import RU
import sys

def main():

    args = sys.argv
    if len(args) != 3:
        print( f"{args[0]} [Input RU file] [AREA code]" )
        sys.exit()

    rufile = args[1]
    areacode = args[2]

    ru = RU( rufile )

#    year = ru.data( "announced_date/year" )
#    mon = ru.data( "announced_date/mon" )
#    day = ru.data( "announced_date/day" )
#    hour = ru.data( "announced_date/hour" )
#    mins = ru.data( "announced_date/min" )
#    sec = ru.data( "announced_date/sec" )

    count = ru.data( "point_count" )

    for i in range( 0, count ):
        area = ru.data( f"/point_data/{i}/AREA" )
        if area != areacode:
            continue

        fcount = ru.data( f"/point_data/{i}/FCST_count" )
        for t in range(0, fcount):

            year = ru.data( "/point_data/{:}/FCST/{:}/valid_date/year".format(i, t) )
            mon = ru.data( "/point_data/{:}/FCST/{:}/valid_date/mon".format(i, t) )
            day = ru.data( "/point_data/{:}/FCST/{:}/valid_date/day".format(i, t) )
            hour = ru.data( "/point_data/{:}/FCST/{:}/valid_date/hour".format(i, t) )
            mmin = ru.data( "/point_data/{:}/FCST/{:}/valid_date/min".format(i, t) )

            sgfhgt  = ru.data( "/point_data/{:}/FCST/{:}/SGFHGT".format(i, t) ) * 0.1
            sgfper  = ru.data( "/point_data/{:}/FCST/{:}/SGFPER".format(i, t) )

            print( "{:04d}/{:02d}/{:02d} {:02d}:{:02d},{:.2f},{:.2f}".format(year,mon,day,hour,mmin,sgfhgt,sgfper) )


if __name__ == "__main__":
    main()