/*
 * stringBuffer.h
 *
 *  Created on: 2012-11-7
 *      Author: Administrator
 */

#ifndef STRINGBUFFER_H_
#define STRINGBUFFER_H_
#include<iostream>
#include <string>
using namespace std;
class StringBuffer{
private:
	string data;
	int index;
public:
	StringBuffer(string& s){
		this->data = s;
		this->index = 0;
	}
	StringBuffer(const char *s): data(s),index(0){}
	StringBuffer():index(0){}
	bool eof(){
		return this->index == this->data.length();
	}
	char peek(){
		if (! this->eof()){
			return this->data[this->index];
		}
		return '\0';
	}
	string get(int len){
		int temp = this->index;
		this->index += len;
		return this->data.substr(temp, len);
	}
	string get_upto(const char ch){
		size_t end = this->data.find(ch, this->index);
		int temp = this->index;
		this->index = end+1;
		return this->data.substr(temp,end-temp);
	}
};

#endif /* STRINGBUFFER_H_ */
