#include<iostream>
#include<string>
#include<fstream>
#include"python2.7/Python.h"
using namespace std;
int main(int argc,char *argv[])
{
	cout<<"Data Miner version 1.0\n";
	Py_SetProgramName(argv[0]);
	Py_Initialize();
	PyRun_SimpleFile(fopen("./Desktop/tweet_stream.py","r"),"tweet_stream.py");
	Py_Finalize();
}
