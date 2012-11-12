/*
 * torrent.cpp
 *
 *  Created on: 2012-11-7
 *      Author: Administrator
 */

#include "torrent.h"
void Torrent::load_string(string& s){
	this->buffer = StringBuffer(s);
	this->info=this->parse();
}
void Torrent::load_file(const char *filename){
	int length;
	char *t;
	ifstream in(filename, ios::binary);  /* otherwise ,you can't read more than one line */
	in.seekg(0, ios::end);
	length = in.tellg();
	in.seekg(0, ios::beg);
	t = new char[length+1];
	in.read(t, length);
	cout << in.gcount();
	in.close();
	t[length]= 0;
	this->buffer = StringBuffer(t);
	this->info = this->parse();
}
be_node* Torrent::parse(){
	be_node *ret;
	switch(this->buffer.peek()){
	case 'l':
		ret =  this->parse_list();
		break;
	case 'i':
		ret = this->parse_int();
		break;
	case 'd':
		ret =  this->parse_dict();
		break;
	default:
		ret =  this->parse_string();
		break;
	}
	return ret;
}
// string : nn:xxx
be_node* Torrent::parse_string(){
	int len;
	be_node* ret = new be_node();
	ret->type=BE_STR;
	string s = this->buffer.get_upto(':');
	len = atoi(s.c_str());
	ret->s =  new string(this->buffer.get(len));
	return ret;
}
// integer: ixxxxe
be_node* Torrent::parse_int(){
	be_node* ret = new be_node();
	this->buffer.get(1);
	ret->type=BE_INT;
	ret->i=new string(this->buffer.get_upto('e'));
	return ret;
}
// list : lxxxe
be_node* Torrent::parse_list(){
	be_node* ret = new be_node();
	ret->type = BE_LIST;
	ret->l = new vector<be_node*>();
	this->buffer.get(1);
	while(this->buffer.peek() != 'e'){
		ret->l->push_back(this->parse());
	}
	this->buffer.get(1);
	return ret;
}
be_node* Torrent::parse_dict(){
	be_node *ret = new be_node() ;
	be_node *key;
	be_node *value;
	string skey;
	ret->type = BE_DICT;
	ret->d = new map<string , be_node*>();
	this->buffer.get(1);
	while(this->buffer.peek() != 'e'){
		key = this->parse_string();
		value = this->parse();
		skey = key->s->c_str();
		ret->d->insert(make_pair(skey, value));
	}
	this->buffer.get(1);
	return ret;
}
ostream& Torrent::serialize(struct be_node* obj, ostream & sout){
	vector<be_node* >::iterator itl;
	map<string, be_node*>::iterator itd;
	switch(obj->type){
	case BE_LIST:
		sout << 'l';
		for(itl=obj->l->begin(); itl != obj->l->end(); ++itl){
			serialize(*itl,sout);
		}
		sout << 'e';
		break;
	case BE_INT:
		sout << 'i' << (*obj->i)<< 'e';
		break;
	case BE_DICT:
		sout << 'd';
		for(itd=obj->d->begin(); itd != obj->d->end(); ++itd){
			sout << (itd->first).length() << ':' << itd->first;
			serialize(itd->second, sout);
		}
		sout <<'e';
		break;
	default:   // string nn:xxxx
		sout << obj->s->length() << ':' << (*obj->s) ;
		break;
	}
	return sout;
}

void Torrent::display(be_node *obj){
	vector<be_node* >::iterator itl;
	map<string, be_node*>::iterator itd;
	switch(obj->type){
	case BE_LIST:
		cout << 'l' <<endl;;
		for(itl=obj->l->begin(); itl != obj->l->end(); ++itl){
			display(*itl);
		}
		cout << 'e' << endl;
		break;
	case BE_INT:
		cout << 'i' << (*obj->i)<< 'e'<<endl;;
		break;
	case BE_DICT:
		cout << 'd'<<endl;
		for(itd=obj->d->begin(); itd != obj->d->end(); ++itd){
			cout << itd->first;
			display(itd->second);
		}
		cout <<'e' << endl;
		break;
	default:   // string nn:xxxx
		cout << obj->s->length() << ':' << (*obj->s) << endl ;
		break;
	}
}
string Torrent::dump_to_string(){
	ostringstream sout;
	serialize(info, sout);
	return sout.str();
}
void Torrent::dum_to_file(const char *fname){
	ofstream fout(fname, ios_base::out|ios::binary);
	serialize(info, fout);
	fout.flush();
	fout.close();
}
void  Torrent::dump_to_file(const string& fname){
	dum_to_file(fname.c_str());

}
void Torrent::set_trackers(const string& trackers){
	char tracker[256];
	bool b_announce = true; // indicate to set announce or annouce-list
	be_node * node;
	be_node *ls;
	streamsize cnt;
	istringstream sin(trackers);
	while(!sin.eof()){
		sin.getline(tracker, 256);
		cnt = sin.gcount();  // char count including \n
		if(tracker[cnt-2] == '\r'){
			tracker[cnt-2] = '\0';
		}
		node = new be_node();
		node->type = BE_STR;
		node->s = new string(tracker);
		if(b_announce){
			(*info->d)["announce"] = node;
			b_announce = false;
		}else{ // each item in announce-list is a be_list with just one item be_str

			ls = new be_node();
			ls->type = BE_LIST;
			ls->l = new vector<be_node*>();
			ls->l->push_back(node);
			node = (*info->d)["announce-list"];
			node->l->push_back(ls);
		}
	}
}


