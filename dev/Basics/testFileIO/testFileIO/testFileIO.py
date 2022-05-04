import pickle
import uuid


class OreOre():
    def __init__(self, aaa_, bbb_):
        self.aaa = aaa_
        self.bbb = bbb_
        self.ccc = (-565, 'Z', uuid.uuid1())




if __name__ == "__main__":

    ################### pickleで保存 #######################
    D = ( 'CreateNode', OreOre(5.5,'gfdsgfdgfds') )#{'a':1, 'b':2}
    D2 = ( 'Connect', OreOre(-68.2,'------y542qi-hy42') )

    F = open('dump.pkl', 'wb')
    pickle.dump(D, F)          # pickleでシリアライズ
    pickle.dump(D2, F)          # pickleでシリアライズ
    F.close()

    ################## pickleからロード #####################
    objects = []
    with(open("dump.pkl", "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))# pickleでデシリアライズしてリストに追加する
            except EOFError:
                break

    for obj in objects:
        print( obj[0] )