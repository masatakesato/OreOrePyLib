import datetime
import BalloonTip


if __name__ == "__main__":

    d = datetime.datetime.today()
    tstr = d.strftime( "%Y/%m/%d %H:%M:%S" )

    BalloonTip.balloon_tip( "現在の時刻", tstr )