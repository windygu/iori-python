/*
 * torrent.h
 *
 *  Created on: 2012-11-7
 *      Author: Administrator
 */

#ifndef TORRENT_H_
#define TORRENT_H_
#include<string>
#include <vector>
#include<iostream>
#include<fstream>
#include<sstream>
#include <map>
#include<cstdlib>
#include "stringBuffer.h"
using namespace std;
typedef enum {
	BE_STR,
	BE_INT,
	BE_LIST,
	BE_DICT,
}be_type;
class be_node;
class string_compare{
public:
	bool operator()(const string& left, const string& right)const{
		return left.compare(right) == 0;
	}
};
class be_node{
public:
	be_type type;
	union{
		string *s;
		string *i;
		vector<be_node*> *l;
		map<string ,be_node*>*d;
	};
};

class Torrent{
public:
	void load_string(string& s);
	void load_file(const char *filename);
	be_node* parse();
	be_node* parse_string();
	be_node* parse_int();
	be_node* parse_list();
	be_node* parse_dict();
	ostream& serialize(be_node* obj, ostream & sout);
	void display(be_node *obj);
	void disp(){ display(info);}
	string dump_to_string();
	void dum_to_file(const char *fname);
	void  dump_to_file(const string& fname);
	void set_trackers(const string& trackers);
private:
	be_node* info;
	StringBuffer buffer;
};

#endif /* TORRENT_H_ */
