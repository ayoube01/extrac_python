#extract files and using list of list
import os
import sys
import csv
from statistics import mean
from numpy import *
argument=sys.argv[1:]
def parcourir(src):
        fichier=[]
        fichier_traite=[]
        myfile=[]
        valeur=[]
        valeur_execution=[]
        mini=[]
        maxi=[]
        meani_=[]
        std_=[]#pour calculer le std le premier h
        convergence=[]
        
        liste_fichier_src=os.listdir(src)
        nb_fichier=len(liste_fichier_src)
        for i in range(0,nb_fichier):
            if "DockingRes" in liste_fichier_src[i]:
                fichier.append(os.path.join(src,liste_fichier_src[i]))
        for i in range(0,len(fichier)):
            fichier_traite.append(os.path.join(fichier[i],"QuantumDocking.out"))
            fichier_traite[i]=os.path.abspath(fichier_traite[i])
            
        for i in range(0,len(fichier_traite)):
            myfile=open(fichier_traite[i])
            for line in myfile:
                if line.find('Total time')!=-1:
                    i1=line.find(":")
                    i2=line.find("h")
                    valeur_heure=float(line[i1+2:i2])
                    i1=line.find("h")
                    i2=line.find("mn")
                    valeur_minute=float(line[i1+2:i2])
                    i1=line.find("mn")
                    i2=line.find("s")
                    valeur_seconde=float(line[i1+2:i2])
                    valeur_execution.append(valeur_heure*3600+valeur_minute*60+valeur_seconde)
                    
                if line.find('Best of the whole RUN')!=-1:
                    i1=line.find(":")
                    i2=line.find("kcal")
                    valeur.append([])
                    valeur[i].append(float(line[i1+2:i2]))
                    std_.append(valeur[i])
            mini.append(min(valeur[i]))
            maxi.append(max(valeur[i]))
            meani_.append(mean(valeur[i]))
            for j in range(len(valeur[i]),0,-1):
                    if valeur[i][j-1]!=valeur[i][j-2]:
                            convergence.append(j)
                            break
        mini=min(mini)
        maxi=max(maxi)
        meani=0
        for j in range(0,len(meani_)):
            meani=meani+meani_[j]
        meani=meani/len(meani_)
        
        mini_mini=min(convergence)
        maxi_maxi=max(convergence)        
        meani_meani=0
        for j in range(0,len(convergence)):
                meani_meani=meani_meani+convergence[j]
        meani_meani=meani_meani/len(convergence)
        

        mini_mini_mini=min(valeur_execution)
        maxi_maxi_maxi=max(valeur_execution)
        meani_meani_meani=0
        for j in range(0,len(valeur_execution)):
                meani_meani_meani=meani_meani_meani+valeur_execution[j]
        meani_meani_meani=meani_meani_meani/len(valeur_execution)



        with open('0_InitialData_2ptXO2_0_9_Cauchy_Mut_0_02_10.csv.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter= ';' ,
                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([' ','RUNS'])
                liste=['GENERATION']
                for i in range(1,len(fichier_traite)+1):
                        liste.append(i)
                spamwriter.writerow(liste)
                for j in range(0,len(valeur[0])):
                        liste=[j+1]
                        for i in range(0,len(fichier_traite)):
                                liste.append(valeur[i][j])
                                
                        spamwriter.writerow(liste)

                
                spamwriter.writerow([])
                spamwriter.writerow([' ','ENERGY'])
                spamwriter.writerow(['MIN',mini])
                spamwriter.writerow(['MAX',maxi])
                spamwriter.writerow(['MEAN',meani])
                spamwriter.writerow(['STD',std(std_)])
                spamwriter.writerow([])
                spamwriter.writerow([' ','CONVERGENCE'])
                liste=['Last improvment']
                for i in range(0,len(fichier_traite)):
                        liste.append(convergence[i])
                
                spamwriter.writerow(liste)
                spamwriter.writerow(['MIN',mini_mini])
                spamwriter.writerow(['MAX',maxi_maxi])
                spamwriter.writerow(['MEAN',meani_meani])
                spamwriter.writerow(['STD',std(convergence)])
                spamwriter.writerow([])
                spamwriter.writerow(['  ','TIME(in s)'])
                liste=['TOTAL']
                for i in range(0,len(fichier_traite)):
                        liste.append(valeur_execution[i])
                spamwriter.writerow(liste)
                spamwriter.writerow(['MIN',mini_mini_mini])
                spamwriter.writerow(['MAX',maxi_maxi_maxi])
                spamwriter.writerow(['MEAN',meani_meani_meani])
                spamwriter.writerow(['STD',std(valeur_execution)])
        return 
src=argument[0]
parcourir(src)
 
