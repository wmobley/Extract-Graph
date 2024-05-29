import ollama
import json as j

# Just runs .complete to make sure the LLM is listening
from llama_index.llms import Ollama
from pathlib import Path
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional, Sequence
from llama_index import (
    VectorStoreIndex,
    ServiceContext,
    download_loader,
VectorStoreIndex,
SimpleDirectoryReader
)
from llama_index.storage.storage_context import StorageContext
llm = Ollama(model="mixtral")
import pandas as pd
import json as j
from typing import List, Optional, Dict, Union
import sys 
import random
random.seed(11434)
from pathlib import Path
# Specify the file you want to read
from neo4j import GraphDatabase

def clean_list_string(x):
    try:
        p= f'[{x.split("[")[1].split("]")[0]}]'
        return eval(p)
    except: 
        return  None
          
def clean_dict_string(x):
    try:
        p= "{"+'}'.join('{'.join(response.response.split("{")[1:]).split("}")[:-1])+"}"
        return eval(p)
    except: 
        print(response.response)
        pass



class Neo4jDatabase:
    def __init__(self, uri, user, password):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None

        
    def close(self):
        if self._driver is not None:
            self._driver.close()

    def connect(self):
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))

    def query_node(self, node):
        query = f"MATCH (n:{node}) RETURN n;"
        self.connect()
        response = self._driver.execute_query(query,database_="neo4j")
        self.close()
        return response

    def previous_node_names(self, node):
        previous_framework = []
        for record in self.query_node(node).records:
            
            previous_framework.append(record['n']._properties['Name'])
        return previous_framework

    
    def create_uncertainty(self, data):
        query = (
            """MERGE (m:uncertainty {Name: $name})
               SET
               m.Name=$name,
               m.Definition=$definition,
               m.Level=$level;"""
        )
        self.connect()
        self._driver.execute_query(query,
                                   name = data['Name'], 
                                   definition=  data['Definition'], 
                                   level = data['Level'], 
                                   database_="neo4j",)
        self.close()
    
    def create_techniques(self, data):
        query = (
            """MERGE (m:techniques {Name: ($Name)})
            SET
            m.Name=$Name,
            m.Description=$Description,
            m.Limitations=$Limitations,
            m.Constraints=$Constraints,
            m.Sampling=$Sampling,
            m.Optimization=$Optimization,
            m.Reduction=$Reduction,
            m.Machinelearning = $Machinelearning;"""
        )
        self.connect()
        self._driver.execute_query(query,
                                   Name = data['Name'], 
                                   Description=  data['Description'], 
                                   Limitations = data['Limitations'], 
                                   Constraints = data['Constraints'], 
                                   Sampling = data['Sampling'], 
                                   Optimization = data['Optimization'], 
                                   Reduction= data['Reduction'],
                                   Machinelearning = data['Machinelearning'], 
                                   database_="neo4j",)
        self.close()

    def create_steps(self, data):
        query = (
            """MERGE (m:steps {Name: ($Name)})
            SET
                m.Name=$Name,
                m.Description=$Description,
                m.Limitations=$Limitations,
                m.Constraints=$Constraints;"""
        )
        self.connect()
        self._driver.execute_query(query,
                                   Name = data['Name'], 
                                   Description=  data['Description'], 
                                   Limitations = data['Limitations'], 
                                   Constraints = data['Constraints'], 
                                   database_="neo4j",)
        self.close()
    
    def create_software(self, data):
        query = (
            """MERGE (m:software {Name: ($Name)})
                    SET
                    m.Name=$Name;"""
        )
        self.connect()
        self._driver.execute_query(query,
                                   Name = data['Name'], 
                                   database_="neo4j",)
        self.close()

    def create_Frameworks(self, data):
        query = (
            """MERGE (m:Frameworks {Name: ($Name)})
                    SET
                    m.Name=$Name,
                    m.Acronym=$Acronym,
                    m.Definition=$Definition,
                    m.KeyGoals=$KeyGoals,
                    m.Limitations=$Limitations,
                    m.Applicability=$Applicability,
                    m.UserObjective = $UserObjective;"""
        )
        self.connect()
        self._driver.execute_query(query,
                                   Name = data['Name'], 
                                   Acronym=  data['Acronym'], 
                                   Definition = data['Definition'], 
                                   KeyGoals = data['KeyGoals'], 
                                   Limitations = data['Limitations'], 
                                   Applicability = data['Applicability'], 
                                   UserObjective = data['UserObjective'], 
                                   database_="neo4j",)
        self.close()
    def create_stakeholders(self, data):
        query = (
            """MERGE (m:Stakeholders {Name: ($Name)})
                    SET
                    m.Name=$Name,
                    m.Description=$Description,
                    m.Organization=$Organization;
                    """
        )
        self.connect()
        self._driver.execute_query(query,
                                   Name = data['Name'], 
                                   Description = data['Description'], 
                                   Organization = data['Organization'], 
                                   database_="neo4j",)
        self.close()

    
    def Match_steps(self, data):
        query = (
                """MATCH (p:steps {Name: $Name})
                    MATCH (m:steps {Name: $Related})
                    MERGE (p)-[r:"""+ "".join(data['Predicate'].split(" ")) +"""]->(m);"""
        )
        self.connect()
        self._driver.execute_query(query,
                                   Name = data['Name'], 
                                   Related=  data['Related'], 
                                   database_="neo4j",)
        self.close()
        
    def Match_framework_steps(self, data):
        query = (
                """
                MATCH (p:Frameworks {Name: $Framework})
                MATCH (m:steps {Name: $Step})
                MERGE (m)-[r:UsedIn]->(p);
"""
        )
        self.connect()
        self._driver.execute_query(query,
                                   Framework = data['Framework'], 
                                   Step=  data['Step'], 
                                   database_="neo4j",)
        self.close()


    def Match_steps_techniques(self, data):
        query = (
                """
                MATCH (p:steps {Name: $Step})
                MATCH (m:techniques {Name: $Technique})
                MERGE (p)-[r:CanUse]->(m);
                """
        )
        self.connect()
        self._driver.execute_query(query,
                                   Technique = data['Technique'], 
                                   Step=  data['Step'], 
                                   database_="neo4j",)
        self.close()
    def Match_techniques_software(self, data):
        query = (
                """
                MATCH (p:software {Name: $Software})
                MATCH (m:techniques {Name: $Technique})
                MERGE (p)-[r:supports]->(m);
                """
        )
        self.connect()
        self._driver.execute_query(query,
                                   Technique = data['Technique'], 
                                   Software=  data['Software'], 
                                   database_="neo4j",)
        self.close()

    def create_Citation(self, data):
        query = (
            """MERGE (m:Citation {TextName: ($Name)})
                    SET
                    m.TextName=$Name;
                    """
        )
        self.connect()
        self._driver.execute_query(query,
                                   Name = data['Name'], 
                                   
                                   database_="neo4j",)
        self.close()
    
    def citedby(self, data):
        self.create_Citation(data)
        query = (
                """
                MATCH (p:"""+data['node']+""" {Name: $NodeName})
                MATCH (m:Citation {TextName: $Name})
                MERGE (m)-[r:references]->(p);
                """
        )
        
        self.connect()
        self._driver.execute_query(query,
                                   NodeName = data['NodeName'], 
                                   Name=  data['Name'], 
                                   database_="neo4j",)
        self.close()


    
class Ontology(BaseModel):
    labels: List[Union[str, Dict]]
    relationships: List[str]

    def dump(self):
        if len(self.relationships) == 0:
            return self.model_dump(exclude=["relationships"])
        else:
            return self.model_dump()
    

class Framework(BaseModel):
    """Identifying the frameworks and characteristics listed in the documents"""
    Name: str  = Field(..., description="The name of framework used in the prompt")
    Acronym : str = Field(..., description = "The Acronym used for the Framework")
    Definition: str = Field(..., description="A definition for the framework")
    UserObjective: str = Field(..., description="The reason a user would use this framework")
    KeyGoals: Optional[str] = Field(None, description="The goals for using this framework")
    Limitations: Optional[str] = Field(None, description="The limitations of the framework")
    Applicability: str = Field(..., description="The  conditions that would make the  framework more suitable than other frameworks")

class Steps_nodes(BaseModel):
    """Identifying the frameworks and characteristics listed in the documents"""
    Name: str  = Field(..., description="The name of step described in the text")
    Description: str = Field(..., description="A Description for the step")
    Limitations: str =Field(..., description="Give the step what constraints should we be aware of?")
    Constraints: str = Field(..., description="A Description for the step")

uncertainty_examples =  """{
                Level: 1
                UsesModel: Single Deterministic
                GeneratesOutcome: Point Estimate
                }
                
                {Level: 2
                UsesModel: Single Stochastic
                GeneratesOutcome: Confidence Interval
                }
                
                {Level: 3
                UsesModel: Limited Alternatives
                GeneratesOutcome: Limited Range
                }
                
                {Level: 4
                UsesModel: Multiple Alternatives
                GeneratesOutcome: Wide Range
                }"""
class Uncertainty(BaseModel):
    """Identifying the frameworks and characteristics listed in the documents"""
    Name: str  = Field(..., description="The name of uncertainty described in the text")
    Definition: str = Field(..., description="A definition for the uncertainty")
    Level: int = Field(None, description=f"Level of uncertainty as described through: {uncertainty_examples}")

class Step(BaseModel):
    """Identifying the frameworks and characteristics listed in the documents"""
    Name: str  = Field(..., description="The name of Step described in the query")
    Related: str = Field(..., description="The Name of the related other step described in the list. ")
    Predicate: str =Field(..., description="How the related step is related to the first step. ex. Follows or Uses")

class Steps(BaseModel):
    """Identifying the frameworks and characteristics listed in the documents"""
    steps: List[Step]

class Technique(BaseModel):
    """Identifying the frameworks and characteristics listed in the documents"""
    Name: str  = Field(..., description="The name of Technique described in the text")
    Acronym : str = Field( None, description = "The Acronym used for the Technique")
    Description: str = Field(..., description="A Description for the Technique")
    Limitations: str =Field(..., description="Give the Technique what constraints should we be aware of?")
    Constraints: str = Field(..., description="A Description for the Technique")
    Sampling: bool = Field(None, description="Whether the technique is a sampling approach or not") 
    Optimization: bool = Field(None, description="Whether the technique is an optimizaiton approach or not") 
    Reduction: bool = Field(None, description="Whether the technique is provides information reduction or not") 
    Machinelearning: bool = Field(None, description="Whether the technique is uses machine learning or not") 

class Stakeholder(BaseModel):
    """Identifying the frameworks and characteristics listed in the documents"""
    Name: str  = Field(..., description="The name of Stakeholder described in the text")
    Description: str = Field(..., description="A Description for the Stakeholder")
    Organization: str =Field(..., description="What Type of Organizaiton is the stakeholder a part of. ")


if __name__=='__main__':
    uri = sys.argv[3]
    user = sys.argv[4]
    password = sys.argv[5]
    
    database = Neo4jDatabase(uri, user, password)

    ontology = Ontology(# labels of the entities to be extracted. Can be a string or an object, like the following.
            labels=[
                {"Frameworks": "Conceptual Frameworks used for Decision Making Under Deep Uncertainty. example Robust Decision Making"},
                {"Uncertainty": " Uncertainties and assumptions the documents analyzed"},
                {"Stakeholder": "specific  names of Stakeholders types"},
                {"Steps": 'steps used to assess a framework'},
                {"Technique":"techniques that the documents identify in which the user can perform that will acheive the step"},
                {"Software":'software names that the documents identify'},
               
            ],
            # Relationships that are important for your application.
            # These are more like instructions for the LLM to nudge it to focus on specific relationships.
            # There is no guarentee that only these relationships will be extracted, but some models do a good job overall at sticking to these relations.
            relationships=[
                "Relation between any pair of Entities",
                ],)
    
    text = sys.argv[1]
    workfolder = sys.argv[2]
    reader = SimpleDirectoryReader(input_files=[f'{workfolder}/{text}.pdf'])
    documents = reader.load_data()
    docs = [d.text for d in documents]
    service_context = ServiceContext.from_defaults(llm=llm, embed_model="local:BAAI/bge-small-en")
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(
 "You are an expert at creating Knowledge Graphs. "
            "Consider the following ontology. \n"
            f"{ontology} \n"
            "The user will provide you with an input text delimited by ```. "
            "Extract all the entities and relationships from the user-provided text as per the given ontology. Do not use any previous knowledge about the context."
            "Remember there can be multiple direct (explicit) or implied relationships between the same pair of nodes. "
            "Be consistent with the given ontology. Use ONLY the labels and relationships mentioned in the ontology. "
            "Format your output as a json with the following schema. \n"
            "[\n"
            "   {\n"
            '       node_1: Required, an entity object with attributes: {"label": "as per the ontology", "name": "Name of the entity"},\n'
            '       node_2: Required, an entity object with attributes: {"label": "as per the ontology", "name": "Name of the entity"},\n'
            "       relationship: Describe the relationship between node_1 and node_2 as per the context, in a few sentences.\n"
            "   },\n"
            "]\n"
            "Do not add any other comment before or after the json. Respond ONLY with a well formed json that can be directly read by a program."
        )
    
    
    nodes = {}
    for q in ['Frameworks','Uncertainty','Stakeholders']:
        # previous_nodes = database.previous_node_names(q)
        questions = {"Frameworks":f"Create a graph network by providing a generalizable list of nodes related to Conceptual Frameworks used for Decision Making Under Deep Uncertainty. example Robust Decision Making.\
        Write the list as a python array",
                "Uncertainty":f"Create a graph network by providing a list of  Uncertainties and assumptions the documents analyzed.\
Write the list as a python array" ,
                "Stakeholders":f"Create a graph network by providing a list of specific  names of Stakeholders types. \
 Write the list as a python array"}
        response = query_engine.query(questions[q])
        nodes.update({q: clean_list_string(response.response)})
    steps = []
    # previous_nodes =database.previous_node_names("Steps")
    
    steps_names = []
    if nodes['Frameworks'] is not None:
        for node in nodes['Frameworks']:
            response = query_engine.query(f"Provide a list of steps used to perform the  following: {node}.Write the list as a python array. If there are no relevant steps provide an empty array []")
            response_list = clean_list_string(response.response)
            steps_names.append(response_list)
            steps.append({node:response_list})
        nodes.update({"Steps": steps}) 
    
    instructions ="Do not write any unicode text. \n Write the list as a single python array.\n If no techniques are relevant to the step provide an empty array []. "


    techniques = []
    # previous_nodes =database.previous_node_names("Techniques")
    
    for framework in nodes['Steps']:
        for key in framework.keys():
            if framework[key] is not None:
                for node in framework[key]:
                    response = query_engine.query(f"The user will be running the following step: {node}. Provide a single list of  techniques that the documents identify in which the user can perform that will acheive the step.\
                    Examples include but are not limited to: Real Options Analysis (ROA), Options Analysis (EOA), \
                    Latin Hyper Cube Sampling,  Adaptation Tipping Points (ATPs), Mult Objective Optimization Analysis,\
                    Ensemble Forecasting.\
                     \n\n\n{instructions}" )
                    response_list = clean_list_string(response.response)
                    techniques.append({node: response_list})
    nodes.update({"Techniques": techniques})


    duplicate_technique = []
    software =[]
    # previous_nodes =database.previous_node_names("Software")
    
    for node in nodes[ 'Techniques']:
            for key in node.keys():
                if node[key] is not None:
                    for technique in node[key]:
                        if technique in duplicate_technique:continue
                        else: duplicate_technique.append(technique)
                        response = query_engine.query(f'The user will be running the following technique: {technique}. \
                        Provide a single list of software names that the documents identify in which the user can perform that will achieve the step.Examples include Pathways Generator, Vensim, Excel Do not provide citations. If the documents do not explicitly mention a software for the technique provide an empty array.\
                       {instructions}')
                        response_list = clean_list_string(response.response)
                        software.append({technique:response_list})           
    nodes.update({"Software": software})
    


    instructions ="Provide a short concise answer. Do not use unicode Text"

    
    query_engine = index.as_query_engine(output_cls=Framework)
    frameworks = {}
    key = 'Frameworks'
    frameworks.update({key:[]})
    keywords =[]
    for Keyword in nodes[key]:
        if Keyword in keywords:continue
        else: keywords.append(Keyword)
        try:
            definition = query_engine.query(f'Describe the following {Keyword} in the context of DMDU. \n {instructions}')
        except: print(f"{Keyword}: Broke")
        definition.response.Name=Keyword
        frameworks[key].append(definition.response.__dict__)
    
    step_list = []
    key ="Steps"   
    query_engine = index.as_query_engine(output_cls=Steps_nodes)
    frameworks.update({key:[]})
    for Keyword in nodes[key]:
        for key_ in Keyword.keys():
           if Keyword[key_] is None: continue
           for step in Keyword[key_]: 
                if step in step_list: continue
                else: step_list.append(step)
                try:
                    description = query_engine.query(f' Describe the following step: {step}.Include the description, limitations, and constraints. \n {instructions}')
                except: continue 
                description.response.Name=step
                frameworks[key].append(description.response.__dict__)

    
    query_engine = index.as_query_engine(output_cls=Uncertainty)
    key = 'Uncertainty'
    frameworks.update({key:[]})
    if nodes[key] is not None:
        for Keyword in nodes[key]:
            try:
                definition = query_engine.query(f'Describe {Keyword} as an uncertainty. Including the name, Definition, and Level based on the follwowing examples: {uncertainty_examples}\n {instructions}')
            except: print(f"{Keyword}: Broke")
            definition.response.Name=Keyword
            frameworks[key].append(definition.response.__dict__)



    step_edges = []
    key = 'Steps'   
    query_engine = index.as_query_engine(output_cls=Steps)
    for Keyword in nodes[key]:
        for key_ in Keyword.keys():
           if Keyword[key_] is None: continue
           for step_keyword in Keyword[key_]: 
                try:
                    response = query_engine.query(f"Describe how the following step:  {step_keyword}, directly relates to  the other steps:    {', '.join(Keyword[key_])}")
                except:continue 
                for step in response.response.__dict__['steps']: 
                    step.Name = step_keyword
                    step_edges.append(step.__dict__)
        
    pd.DataFrame.from_records((step_edges)).to_csv( f"Outputs/{text}step_edges.csv")
    with open(f"Outputs/{text}_step_framework.csv", "a") as f:
        f.write("Framework, Step\n")
    for item in nodes['Steps']:
        for key, step_list in item.items():
            if step_list is None: continue
    
            for step in step_list:
                with open(f"Outputs/{text}_step_framework.csv", "a") as f:
                    f.write(f"{key}, {step}\n")
    with open(f"Outputs/{text}_step_techniques.csv", "w") as f:
        f.write("Step, Technique\n")
    for item in nodes['Techniques']:
        for key, step_list in item.items():
            if step_list is None: continue
            for step in step_list:
                with open(f"Outputs/{text}_step_techniques.csv", "a") as f:
                    f.write(f"{key}, {step}\n")
    with open(f"Outputs/{text}_techniques_software.csv", "w") as f:
        f.write("Technique, Software\n")
    for item in nodes['Techniques']:
        for key, step_list in item.items():
            if step_list is None: continue
            for step in step_list:
                with open(f"Outputs/{text}_techniques_software.csv", "a") as f:
                    f.write(f"{key}, {step}\n")
    pd.DataFrame.from_records((step_edges)).to_csv(f"Outputs/{text}step_edges.csv")


    technique_name =[]
    key ="Techniques"
    frameworks.update({key:[]})
    
    query_engine = index.as_query_engine(output_cls=Technique)
    for Keyword in nodes[key]:
        for keyword_key , item in Keyword.items():
            if item is None: continue
            for technique in item: 
                if technique in technique_name:continue
                else: technique_name.append(technique)
                Description = query_engine.query(f' Describe the following step: {technique}.Include the description, limitations, and constraints.\
                Provide booleans for whether the technique is a sampling approach, optimization approach, use information reduction or machinelearning\n {instructions}')
                Description.response.Name = technique
                frameworks[key].append(Description.response.__dict__)



    key ="Software"
    software = []
    frameworks.update({key:[]})
    for Keyword in nodes["Software"]:
        for keyword_key , items in Keyword.items():
            if items is None: continue
            for item in items: 
                if item in software: continue
                else: software.append(item)
                frameworks[key].append(    {
              "Node": "Software",
              "Name": item,
            })


    
    query_engine = index.as_query_engine(output_cls=Stakeholder)
    key = "Stakeholders"
    frameworks.update({key:[]})
    for Keyword in nodes[key]:
        try:
            description = query_engine.query(f"Describe the stakeholder  {Keyword}")
        except:
                print(f"Broken {Keyword}")        
                continue
        description.response.Name = Keyword
        frameworks[key].append(description.response.__dict__)

    for key in frameworks.keys():
        pd.DataFrame.from_dict(frameworks[key]).to_csv(f"Outputs/{text}{key}.csv")


    for data in frameworks['Frameworks']:
        database.create_Frameworks(data)
        database.citedby({"node":'Frameworks',"Name":text, "NodeName":data['Name']})
    for data in frameworks['Uncertainty']:
        database.create_uncertainty(data)
        database.citedby({"node":"Uncertainty","Name":text, "NodeName":data['Name']})
    
    for data in frameworks['Steps']:
        database.create_steps(data)
        database.citedby({"node":"Steps","Name":text, "NodeName":data['Name']})
    
    for data in frameworks['Techniques']:
        database.create_techniques(data)
        database.citedby({"node":"Steps","Name":text, "NodeName":data['Name']})
    
    for data in frameworks['Software']:
        database.create_software(data)
        database.citedby({"node":"Software","Name":text, "NodeName":data['Name']})
    
    for data in frameworks['Stakeholders']:
        database.create_stakeholders(data)
        database.citedby({"node":"Stakeholders","Name":text, "NodeName":data['Name']})

    for item in nodes['Steps']:
        for key, step_list in item.items():
            if step_list is None: continue
    
            for step in step_list:
                database.Match_framework_steps({"Step":step, "Framework":key})
    
    for item in nodes['Techniques']:
        for key, step_list in item.items():
            if step_list is None: continue
            for step in step_list:
                database.Match_steps_techniques({"Step":key, "Technique":step})
                
    
    for item in nodes['Software']:
        for key, step_list in item.items():
            if step_list is None: continue
            for step in step_list:
              database.Match_techniques_software({"Software":step, "Technique":key})
    
    for s in step_edges:
        if s['Predicate']=="N/A":continue
        try:
            database.Match_steps(s)
        except: continue
