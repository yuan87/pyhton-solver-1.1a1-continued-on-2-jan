import sys
import pandas as pd
import csv
import os
import gc
import pickle
import json
# case_solver class and case_reader class
# from pkg.calcsolve import case_solver
# from pkg.calcsolve import case_reader
from .calcsolve import *



gc.enable()


class CaseSceneIns():
    '''
    This class functions as create instances of case_reader and case_solver, ie: create creating different case
    Define working condition and cases here
    '''

    def __init__(self,path_text):

        # path0=str(os.path.dirname(os.path.abspath(__file__)))
        # path=path.replace('\\','/')+'/'
        self.path_text=path_text

        file_names=[
            'main.csv',
            'mast_achor_conf.csv',
            'misc.csv',
            'dictionary.json',
            'crane/',
            '.csv',
            'mast/mast.csv',
            'wind section/wind_section.csv'
            ]

        caseReader=case_reader(self.path_text,file_names[0],file_names[1],file_names[2],file_names[3],file_names[4],file_names[5],file_names[6],file_names[7])
        # unpickle
        with open(self.path_text+'ReadData.pkl','rb') as r_data:
            dictData=pickle.loads(r_data.read())
        # dictData=caseReader.dictData

        self.run_solve(self.path_text,dictData)


    def run_solve(self,path,dictData):
        # solve for in service and out of service, all anchora tighten and alt released configuration

        inStr="""

____________________________________


        """
        tie_release=0
        strInService='In service'
        strOutOfService='Out of service'

        print(inStr+strInService+' '+'tighten'+inStr)
        solverInTighten=case_solver(
            path,
            dictData.get('Anchorage'),
            dictData.get('Top load in serv'),
            dictData.get('Wind force in serv'),
            dictData.get('Wind force region in'),
            dictData.get('Mast height'),
            dictData.get('Top wind height'),
            tie_release,
            strInService
            )
        rInTighten=solverInTighten.output_table()

        print(inStr+strOutOfService+' '+'tighten'+inStr)
        solverOutTighten=case_solver(
            path,
            dictData.get('Anchorage'),
            dictData.get('Top load out serv'),
            dictData.get('Wind force out serv'),
            dictData.get('Wind force region out'),
            dictData.get('Mast height'),
            dictData.get('Top wind height'),
            tie_release,
            strOutOfService
            )
        # print(dictData.get('Wind force region out'))
        rOutTighten=solverOutTighten.output_table()


        tie_release=1
        print(inStr+strInService+' '+'released'+inStr)
        solverInReleased=case_solver(
            path,
            dictData.get('Anchorage'),
            dictData.get('Top load in serv'),
            dictData.get('Wind force in serv'),
            dictData.get('Wind force region in'),
            dictData.get('Mast height'),
            dictData.get('Top wind height'),
            tie_release,
            strInService
            )
        rInReleased=solverInReleased.output_table()

        print(inStr+strOutOfService+' '+'released'+inStr)
        solverOutReleased=case_solver(
            path,
            dictData.get('Anchorage'),
            dictData.get('Top load out serv'),
            dictData.get('Wind force out serv'),
            dictData.get('Wind force region out'),
            dictData.get('Mast height'),
            dictData.get('Top wind height'),
            tie_release,
            strOutOfService
            )
        rOutReleased=solverOutReleased.output_table()

        self.dictData=dictData
        self.rList=[rInTighten,rOutTighten,rInReleased,rOutReleased]

    def get_result(self):
        return str(self.dictData.get('Mast height')),self.rList




gc.collect()
