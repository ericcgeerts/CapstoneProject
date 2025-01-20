import math
from amplpy import AMPL, Environment, DataFrame
import pandas as pd
import numpy as np

##Load the Student data and wieghts data, student data location is based on the .txt saves for the filepath that occured in the application
Weightsdata = np.loadtxt('Weights.csv', delimiter=',')
FilePath = np.loadtxt('Filepath.txt')
StudentData = np.loadtxt(Filepath, delimiter=',')

files = [Weightsdata,StudentData]

##Execute group formation algorithim
g = 0
df_firstparams = Weightsdata[0]
if df_firstparams.iat[0,1] != 0:
  g = 1
groupSize = df_firstparams.iat[0,2]
maxGroupSize = df_firstparams.iat[0,3]

df_secondparams = Weightsdata[1]
diversity_files = []
weights = []
for i in range(df_secondparams.shape[0]):
  file_name = df_secondparams.iat[i,0]
  diversity_files.append(file_name)
  weight = df_secondparams.iat[i,2]
  weights.append(weight)

weight_params = ""#done
diversity_params = ""#done
gender_params = ""#done

x_variable = ""#done
diversity_variables = ""#done
gender_variable = ""#done
obj_function = ""#done

diversity_constraints = ""#done
gender_constraint = ""#done
assignment_constraints = ""#done

weight_names = []
for j in range(len(weights)):
  name = "importance" + str(j+1)
  weight_names.append(name)
  weight_params += "param " + str(name) + ";\n"

if g == 1:
  df_gender = pd.read_csv(files[2].format(Weightsdata)
  df_gender = df_gender.head(30)
  i = df_gender.shape[0]
  j = math.floor(i/groupSize)
  k = df_gender.shape[1]
  gender_params = "param gender{i in 1.." + str(i) + ", k in 1.." + str(k) + "} binary;\n"
  gender_variable = "var g{j in 1.." + str(j) + "} binary;\n"
  gender_constraint = '''subject to noIsoLadies1{j in 1..'''+str(j)+'''}:
  2*g[j] <= sum{i in 1..'''+str(i)+'''} x[i,j]*(gender[i,2]+gender[i,3]);\nsubject to noIsoLadies2{j in 1..'''+str(j)+'''}:
  sum{i in 1..'''+str(i)+'''} x[i,j]*(gender[i,2]+gender[i,3]) <= groupSize*g[j];\n'''

counter = 0
for f in range(len(diversity_files)):
  counter += 1

  file_name = diversity_files[f]
  df = pd.read_csv(file_name.format(data_dir))
  df = df.head(30)
  i = df.shape[0]
  j = math.floor(i/groupSize)
  k = df.shape[1])

  if counter == 1:
    x_variable = "var x{i in 1.."+str(i)+", j in 1.."+str(j)+"} binary;\n"
    obj_function = "maximize z: (sum{j in 1.."+str(j)+", k in 1.."+str(k)+"}("+weight_names[counter-1]+"*y"+str(counter)+"[j,k]) + "
  elif 1 < counter < len(diversity_files):
    obj_function += "sum{j in 1.."+str(j)+", k in 1.."+str(k)+"}("+weight_names[counter-1]+"*y"+str(counter)+"[j,k]) + "
    #obj_function += "+ "+weight_names[counter-1]+"*y"+str(counter)+"[j,k] "
  else:
    obj_function += "sum{j in 1.."+str(j)+", k in 1.."+str(k)+"}("+weight_names[counter-1]+"*y"+str(counter)+"[j,k]));\n"

  diversity_params += "param " + file_names[f+3] + "{i in 1.." + str(i) + ", k in 1.." + str(k) + "} binary;\n"
  diversity_variables += "var y" + str(counter) + "{j in 1.."+str(j)+", k in 1.."+str(k)+"} binary;\n"
  diversity_constraints += '''subject to diversity''' + str(counter) + '''{j in 1..'''+str(j)+''', k in 1..'''+str(k)+'''}:
  y'''+str(counter)+'''[j,k] <= sum{i in 1..'''+str(i)+'''} x[i,j]*'''+file_names[f+3]+'''[i,k];\n'''


assignment_constraints = '''subject to allStudentsAssigned{i in 1..'''+str(i)+'''}: sum{j in 1..'''+str(j)+'''} x[i,j] == 1;
subject to teamSizeLower{j in 1..'''+str(j)+'''}: sum{i in 1..'''+str(i)+'''} x[i,j] >= groupSize;
subject to teamSizeUpper{j in 1..'''+str(j)+'''}: sum{i in 1..'''+str(i)+'''} x[i,j] <= maxGroupSize+1;'''

ampl_string = '''param classSize;
param groupSize;
param maxGroupSize;
param numberOfGroups;
'''+ weight_params + diversity_params + gender_params + x_variable + diversity_variables + gender_variable + obj_function + diversity_constraints + gender_constraint + assignment_constraints

print(ampl_string)
##Optimization Problem Defenition
ampl.eval(ampl_string)

##Model Parameters
classSize = i
numberOfGroups = j

ampl.getParameter('classSize').set(classSize)
ampl.getParameter('groupSize').set(int(groupSize))
ampl.getParameter('maxGroupSize').set(int(maxGroupSize))
ampl.getParameter('numberOfGroups').set(numberOfGroups)

##Model Paramters
for w in range(len(weight_names)):
  name = "importance" + str(w+1)
  ampl.getParameter('importance' + str(w+1)).set(int(weights[w]))

for f in range(len(diversity_files)):
  #file_name = files[f].split("\\")[-1]
  file_name = diversity_files[f]
  df = pd.read_csv(file_name.format(data_dir))
  df = df.head(30)
  i = df.shape[0]
  k = df.shape[1]
  for m in range(i):
    for n in range(k):
      ampl.param[file_names[f+3]][m+1,n+1] = int(df.iat[m,n])

if g ==1:
  df = pd.read_csv(files[2].format(data_dir))
  df = df.head(30)
  i = df.shape[0]
  k = df.shape[1]
  for m in range(i):
    for n in range(k):
      ampl.param['gender'][m+1,n+1] = int(df.iat[m,n])

##Solve and output results
##Student I Group Y should have on Y value where [X,Y] = 1 while others
##are [X,Y] = 0 as a student is in one group

ampl.solve()

for y in range(1,numberOfGroups+1):
  print('\nGroup #' + str(y) + ':')
  for x in range(1,classSize+1):
    if ampl.get_variable('x')[x,y].value() == 1:
      print('-Student #' +  str(x))
###Print to console as well based on stakeholder request
for y in range(1,numberOfGroups+1):
  print('\nGroup #' + str(y) + ':')
  for x in range(1,classSize+1):
    if ampl.get_variable('x')[x,y].value() == 1:
      if ampl.param['gender'][x,1] == 1:
        print('-Student #' +  str(x) + ": boy" )
      elif ampl.param['gender'][x,2] == 1:
        print('-Student #' +  str(x) + ": girl" )
      elif ampl.param['gender'][x,3] == 1:
        print('-Student #' +  str(x) + ": non-binary" )

##Save output of the solved group formation!
np.savetxt("StudentGroups.csv", ampl.solve(), delimiter=",")