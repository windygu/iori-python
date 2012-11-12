#include<strstream>
#include<iostream>
#include<fstream>
#include "torrent.h"

int main(void){
//	string s = "d4:infod5:filesld6:lengthi680126012e4:pathl20:ubuntu.rootfs.tar.gzeed6:lengthi8388608e4:pathl3:img22:ac100-ubuntu-installereeeee";
//	string sres;

//	Torrent torrent ;

//	torrent.load_string(s);

//	sres = torrent.dump_to_string();
//	cout << sres << endl;
	Torrent torrent2;
	string trackers = "one\r\ntwo\r\nthree\r\n";
	torrent2.load_file("test.torrent");
	torrent2.set_trackers(trackers);
	torrent2.disp();
//	torrent2.dump_to_file("out.torrent");
//	map<string ,int> ma;
//	string s= "123";
//	string s2 = "456";
//	ma.insert(make_pair(string(s.c_str()), 5));
//	ma.insert(make_pair(string(s2.c_str()),8 ));
//	cout << ma.size() << endl;


	return 0;

}

