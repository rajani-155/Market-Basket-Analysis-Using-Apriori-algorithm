from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import itertools
from django.contrib import messages
import pandas as pd
import itertools 
import os 
import networkx as nx
import csv
from django.http import HttpResponse
import mplcursors as mpc
import networkx as nx
from matplotlib.font_manager import FontProperties
from django.shortcuts import render
import pandas as pd
import numpy as np
import itertools 
from sys import exit
import matplotlib.pyplot as plt
import seaborn as sns
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse


#taking input for support and confidence


@login_required(login_url='/authentication/login')
def index(request):
    return render(request, 'analysis/home.html', )






def upload_file(request):
    if not os.path.exists('uploads/'):
        os.makedirs('uploads/')

    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            filename = 'file.csv'
            # Save the uploaded file to disk
            file_path = os.path.join('C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\uploads', filename)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            messages.success(request, 'File uploaded successfully.')
            return redirect('upload_file')
        else:
            messages.error(request, 'No file was uploaded.')
    delete_file_and_redirect(request)
    return render(request, 'analysis/upload.html')



    





def delete_file_and_redirect(request):
    # Provide the path to the files you want to delete
    file_paths = [
        "C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\frequent_items\\1-frequent itemset.csv",
        "C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\frequent_items\\2-frequent itemset.csv",
        "C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\frequent_items\\3-frequent itemset.csv",
        "C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\rules.csv",
        "C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\website\\static\\graph\\1-frequent itemset_barplot.jpeg",
        "C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\website\\static\\graph\\2-frequent itemset_barplot.jpeg",
        "C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\website\\static\\graph\\3-frequent itemset_barplot.jpeg",
        "C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\website\\static\\graph\\scatterplot.jpeg",
        "C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\website\\static\\graph\\parallel.jpeg",
        "C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\website\\static\\graph\\heatmap.jpeg",
        "C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\website\\static\\graph\\networkdiagram.jpeg",
        
    ]

    for path in file_paths:
        try:
            # Delete the file
            os.remove(path)
            print("File deleted successfully.")

        except FileNotFoundError:
            print("File not found.")
        except PermissionError:
            print("Permission denied. Unable to delete the file.")
        except Exception as e:
            print("An error occurred:", str(e))

    # Redirect to the desired location
    return redirect('home')  # Replace 'authentication:home' with the appropriate URL name




def rules(request):
        return render(request, 'analysis/analysis.html')

def rule_generation_view(request):
    if request.method == 'POST':
        minsupport = float(request.POST['minsupport'])
        minconfidence = float(request.POST['min_confidence'])
        min_lift = float(request.POST['lift'])

        

    def file_reading():
        global file
        file = open('C:/Users/DELL/OneDrive/Desktop/final_Project/website/uploads/file.csv' ,'r')
        test = file.read()
        return test


    # finding no of transaction
    no_of_transaction = 0
    with open('C:/Users/DELL/OneDrive/Desktop/final_Project/website/uploads/file.csv' , 'r') as fp:
        for line in fp:
            if line != "\n":
                no_of_transaction += 1

    # cleaning


    def cleaning(test):
        test = test.lower()
        words = test.split()
        words = [word.strip('.,!;()[]') for word in words]
        return (words)

    # finding unique item


    def unique_item(words):
        unique = []  # unique item is stored as list
        for word in words:
            if word not in unique:
                unique.append(word)
        unique.sort()
        return (unique)

    # finding frequency of each item(count has the frequency table of the item)


    def first_count(unique, words):
        frequency = []
        for item in unique:
            s = 0
            for a in words:
                if item == a:
                    s += 1
            frequency.append(s)
        return (frequency)


    def join(n, name):
        c2 = []
        for i in range(len(name)):
            j = i+1
            for j in range(i+1, len(name)):
                a = []
                if name[i] != name[j]:
                    a.append(name[i])
                    a.append(name[j])
                c2.append(a)
        c2.sort()
        return c2


    def joining(n, name):
        c3 = []
        for i in range(len(name)-1):
            a = []
            for j in range(i+1, len(name)):
                if len([c for c in name[i] if c in name[j]]) == n-2:
                    a = name[i] + name[j]
                    a.sort()
                    a = [*set(a)]
                if (a != []) and (a not in c3):
                    c3.append(a)
        return c3


    # counting frequency of itemset
    def joining_file_element(n, name):
        file = open('C:/Users/DELL/OneDrive/Desktop/final_Project/website/uploads/file.csv' , 'r')
        list_a = []
        for line in file:
            line = line.lower()
            words = line.split()
            words = [word.strip('.,!;()[]') for word in words]
            words.sort()
            c3 = []
            for i in range(len(words)-(n-1)):
                a = []
                for j in range(i, i+n):
                    a.append(words[j])
                if a not in c3:
                    c3.append(a)
                c3.sort()
            list_a.append(c3)
            flat_list = list(itertools.chain(*list_a))
        counts = []
        for item in name:
            item.sort()
            a = flat_list.count(item)
            counts.append(a)
        return counts

    # support calculation


    def min_support(frequency):
        ms = []
        for item in frequency:
            x = 0
            x = item / no_of_transaction
            ms.append(x)
        return ms

    # printing frequent itemset


    def frequent_item_set(n, name, frequency):
        data = pd.DataFrame(list(zip(name, frequency)),
                            columns=['Name', 'Frequency'])
        counts = min_support(frequency)
        data['Minimun Support'] = counts
        item_set = data.loc[data['Minimun Support'] >= minsupport]
        return item_set


    def scatterplot(rule_set):
        
            s = list(rule_set['Support'])
            c = list(rule_set['Confidence'])
            l =  list(rule_set['Lift'])
            r =  list(rule_set['Rules'])

            #Scatter plot
            plt.figure(figsize=(10,6))
            plt.scatter(s , c, label='Rules', color='blue', s=5)
            plt.grid(True, linestyle='--', color='lightgray', alpha=0.1)
            plt.title('Scatter plot of Support and Confidence ')
            plt.xlabel("Item_Support")
            plt.ylabel("Item_Confidence")
            
            plt.legend()
            imagename = os.path.join('C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\website\\static\\graph', "scatterplot.jpeg") 
            plt.savefig(imagename)
            plt.clf()
        

    def barplot(a,name, frequency):
        for i in range(len(name)):
            name[i] = str(name[i])
        n_bars = len(frequency)
        colors = np.linspace(1, 0.2, n_bars)

        # Adding the values on the bars
        for i, v in enumerate(frequency):
            plt.text(i, v + 0.9, str(v), color='k', ha='center')

        # Setting the margins of x-axis and y-axis separately
        plt.subplots_adjust(left=0.1, bottom=0.3, right=0.9, top=0.9)
        plt.gca().margins(x=0.05, y=0.2)
        plt.bar(name, frequency, color=plt.cm.Blues(
            colors), width=0.9, align='center')
        plt.title("Frequent Item Set", c='blue')
        plt.xticks(rotation=80)
        plt.xlabel("Item_Name",  c='blue')
        plt.ylabel("Item_Frequency",  c='blue')
        imagename = os.path.join('C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\website\\static\\graph', f"{a}-frequent itemset_barplot.jpeg") 
        plt.savefig(imagename)
        plt.clf()


    def parallelplot(rule_set):
        a = list(rule_set["Antecedent"])
        c = list(rule_set["Consequent"])
        l = list(rule_set["Lift"])
        for i in range(len(a)):
            a[i] = str(a[i])
            c[i] = str(c[i])
        data = pd.DataFrame(list(zip(a, c, l)), columns=[
                            'Antecedent', 'Consequent', 'Lift'])
        data = data.round({"Lift": 2})
        fig, ax = plt.subplots()
        pd.plotting.parallel_coordinates(data, 'Lift', ax=ax, cols=[
                                        'Antecedent', 'Consequent'])
        plt.title('Market Basket Analysis')
        imagename = os.path.join('C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\website\\static\\graph', "parallel.jpeg") 
        plt.savefig(imagename)
        plt.clf()


    # taking input for support and confidence
    n = 15
    a = 0
    global item_name, list1
    global mydict
    global rule_name
    rule_name = []
    global min_c
    min_c = []
    a = []
    c = []
    minsu = []
    support_a = []
    support_c = []
    lifts = []
    mydict = {}
    list1 = []
    item_name = []
    item_set = pd.DataFrame()
    for i in range(1, n):
        if i == 1:
            data = file_reading()
            words = cleaning(data)
            name = unique_item(words)
            frequency = first_count(name, words)
            item_set = frequent_item_set(i, name, frequency)
            item_set = item_set.sort_values(by='Frequency', ascending=False)
            item_set.index = np.arange(1, len(item_set)+1)
            if item_set.empty:
                exit
            else:
               
                #print("\n", a, "-frequent itemset ")
                items = item_set.iloc[0: 20]
                filename = os.path.join('C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\frequent_items', f"{i}-frequent itemset.csv") 
                df = pd.DataFrame(items)
                items.to_csv(filename)
                n = list(items["Name"])
                f = list(items["Frequency"])
                barplot(i,n, f)
            item_name = list(item_set["Name"])
            length = len(item_name)
            item_support = list(item_set["Minimun Support"])
            for key in item_name:
                for value in item_support:
                    mydict[key] = value
                    item_support.remove(value)
                    break
            list1.append(item_name)
        else:
            data = file_reading()
            if i == 2:
                name = join(i, list1[i-2])

            else:
                name = joining(i, list1[i-2])
            frequency = joining_file_element(i, name)
            item_set = frequent_item_set(i, name, frequency)
            item_set = item_set.sort_values(by='Frequency', ascending=False)
            item_set.index = np.arange(1, len(item_set)+1)
            if item_set.empty:
                exit
            else:
                #print("\n", a, "-frequent itemset ")
                items = item_set.iloc[0: 20]
                filename = os.path.join('C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\frequent_items', f"{i}-frequent itemset.csv") 
                df = pd.DataFrame(items)
                items.to_csv(filename)
                n = list(items["Name"])
                f = list(items["Frequency"])
                barplot(i,n, f)
            item_name = (list(item_set["Name"]))
            item_support = list(item_set["Minimun Support"])
            for key in item_name:
                for value in item_support:
                    x = tuple(key)
                    mydict[x] = value
                    item_support.remove(value)
                    break
            list1.append(item_name)


    # association rule generatio


    def rule_generation(a_set):
        s = []
        for i in range(1, len(a_set)):
            data = itertools.combinations(a_set, i)
            subsets = set(data)
            l = list(subsets)
            if i == 1:
                l = list(itertools.chain(*l))
            s.append(l)
        flat_list = list(itertools.chain(*s))
        lists = []
        sub = []
        for i in range(len(flat_list)):
            lists.append(flat_list[i])
            temp3 = []
            for element in a_set:
                if element not in flat_list[i]:
                    temp3.append(element)
            if len(temp3) >= 2:
                temp3 = tuple(temp3)
            else:
                temp3 = "".join(temp3)
            sub.append(temp3)

        for i in range(len(lists)):
            if (type(lists[i]) == str) and (type(sub[i]) == str):
                r = lists[i] + " -> " + sub[i]
                if (lists[i] in mydict.keys()) and (sub[i] in mydict.keys()):
                    cf = mydict[a_set]/mydict[lists[i]]
                    cf=round(cf,3)
                    min_c.append(cf)
                    l = mydict[a_set]/(mydict[lists[i]] * mydict[sub[i]])
                    l=round(l,3)
                    minsu.append(mydict[a_set])
                    support_a.append(mydict[lists[i]])
                    support_c.append(mydict[sub[i]])
                    lifts.append(l)
                    rule_name.append(r)
                    a.append(lists[i])
                    c.append(sub[i])

            else:
                s = str(sub[i])
                l = str(lists[i])
                r = l + " -> " + s
                if (lists[i] in mydict.keys()) and (sub[i] in mydict.keys()):
                    cf = mydict[a_set]/mydict[lists[i]]
                    cf=round(cf,3)
                    min_c.append(cf)
                    l = mydict[a_set]/(mydict[lists[i]] * mydict[sub[i]])
                    l=round(l,3)
                    minsu.append(mydict[a_set])
                    support_a.append(mydict[lists[i]])
                    support_c.append(mydict[sub[i]])
                    lifts.append(l)
                    rule_name.append(r)
                    a.append(lists[i])
                    c.append(sub[i])


    def heatmapplot():
        df = pd.read_csv('rules.csv')
        fig, ax = plt.subplots(figsize=(10,10))
        df = df.round({"Lift": 3, "Confidence": 2, "Support": 3})
        couple_columns = df[['Lift', 'Support', 'Confidence']]
        phase_1_2 = couple_columns.groupby(['Support', 'Confidence']).mean()
        phase_1_2 = phase_1_2.reset_index()
        pivot_table = phase_1_2.pivot(
            'Confidence', 'Support', 'Lift').fillna(0)
        # plt.title('HeatMap', size=20)
        plt.xlabel('Support', size=12)
        plt.ylabel('Confidence', size=12)
        a = sns.heatmap(pivot_table, annot=True, fmt=".2f", linewidths=0.5,
                        linecolor='black', square=True, cmap='Greens', ax=ax)
        a.set_yticklabels(a.get_yticklabels(), size=8)

        imagename = os.path.join('C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\website\\static\\graph', "heatmap.jpeg") 
        plt.savefig(imagename)
        plt.clf()
        




    def netdiagram():
        df = pd.read_csv('rules.csv')
        #df = df.iloc[0:11]
        antecedent = list(df['Antecedent'])
        consequent = list(df['Consequent'])
        for item in consequent:
            antecedent.append(item)
        mydict = {}
        y = 1
        for i in range(len(antecedent)):
            if antecedent[i] not in mydict:
                mydict[antecedent[i]] = y
                y = y+1

       
        network = nx.DiGraph()
        color_map = []
        N = 50
        colors = np.random.rand(N)
        x = len(df['Antecedent'])
        strs = []
        for i in range(1, x+1):
            r = "R"+str(i)
            strs.append(r)
        fig, ax = plt.subplots(figsize=(10, 8))

        rules_to_show = 9
        for i in range(rules_to_show):
            r = i+1
            ant = df.loc[i, 'Antecedent']
            network.add_nodes_from(["R"+str(r)])
            network.add_edge(mydict[ant], "R"+str(r), weight=2, color=colors[r])

            con = df.loc[i, 'Consequent']
            network.add_nodes_from(["R"+str(r)])
            network.add_edge("R"+str(r), mydict[con], weight=2, color=colors[r])

        for node in network:
            found_a_string = False
            for item in strs:
                if node == item:
                    found_a_string = True
            if found_a_string:
                color_map.append('#ffcccb')

            else:
                color_map.append('skyblue')

        edges = network.edges()
        colors = [network[u][v]['color'] for u, v in edges]
        weights = [network[u][v]['weight'] for u, v in edges]

        pos = nx.spring_layout(network, k=0.3)


        nx.draw(network, pos, edge_color=colors, arrowsize=20, node_color=color_map, node_size=1700,
                width=weights, font_size=14, with_labels=True, ax=ax)

        for label, text in mydict.items():
            plt.plot([], [], label=f'{text}: {label}',
                    markersize=10, marker='o', linestyle='None', markerfacecolor='skyblue')

        font_props = FontProperties(family='Times New Roman', size=14, weight='bold')

        legend = plt.legend(loc='upper right', title='LEGEND', prop=font_props,
                            title_fontsize=16)

        legend.get_title().set_fontweight('bold')
        plt.title("Top 10 Association Rules", fontsize=20, fontweight='bold')
        plt.tight_layout()        
        
        imagename = os.path.join('C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\website\\static\\graph', "networkdiagram.jpeg") 
        plt.savefig(imagename)
        plt.clf()


    def association_rule(a, c, rule_name, support_a, support_c, minsu, min_c, lifts):
        data = pd.DataFrame(list(zip( rule_name , a , c , support_a, support_c, minsu, min_c, lifts)), columns=[
                            'Rules' , 'Antecedent', 'Consequent', 'Antecedent Support', 'Consequent Support', 'Support', 'Confidence', 'Lift'])
        rules = data.loc[data['Confidence'] >= minconfidence]
        rule_set = rules.loc[rules['Lift'] >= min_lift]
        if rule_set.empty:
            exit
        else:
            print("\n Rules are : ")
            rule_set = rule_set.sort_values(by='Lift', ascending=False)
            rule_set.index = np.arange(1, len(rule_set) + 1)
            rules = rule_set.iloc[0: 15]
            x = len(rule_set["Rules"])
            ind = []
            for i in range(1 , x+1):
                d = "R" + str(i)
                ind.append(d)
            df = pd.DataFrame(rule_set)
            df.insert(0, 'Index', ind)
            df.to_csv('rules.csv', index=False)
            scatterplot(rule_set)
            parallelplot(rules)
            heatmapplot()
            netdiagram()
        """""
            
            df['Antecedent Support'] = np.round(df['Antecedent Support'])
            df['Consequent Support'] = df['Consequent Support'].round(2)

            df['Support'] = df['Support'].round(2)

            df['Confidence'] = df['Confidence'].round(2)

            df['Lift'] = df['Lift'].round(2)
        """""    

            


    n = list(mydict.keys())
    rule_name = []
    for i in range(length, len(n)):
        rule_generation(n[i])

    association_rule(a, c, rule_name, support_a, support_c, minsu, min_c, lifts)

    #return render('home')
    #return HttpResponse("Analysis completed!")  
    print('analysis')
    messages.success(request, 'Analysis completed successfully!')
    return redirect('home')  
        
        
    

def associationrule_table(request):
        with open('rules.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
        return render(request, 'analysis/atable.html', {'data': data})



def frequency_table(request):
    # specify the folder path and get a list of CSV files
    folder_path = 'C:\\Users\\DELL\\OneDrive\\Desktop\\final_Project\\website\\frequent_items'
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # read data from each CSV file and store it in a dictionary
    data = {}
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            data[file] = list(reader)

    # pass the data to the template
    return render(request, 'analysis/ftable.html', {'data': data})

   
        

def scatterplot_view(request):
    return render(request, 'analysis/scatterplot.html')


def barchart_view(request):
    return render(request, 'analysis/bar-chart.html')

def heatmap_view(request):

    return render(request, 'analysis/heatmap.html')


def networkdiagram_view(request):
    return render(request, 'analysis/network.html')


def parallelplot_view(request):
    return render(request, 'analysis/parallel.html')



def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Perform any necessary form validation here
        
        # Example code to send an email
        send_mail(
            'Contact Form Submission',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            'shrestarajani155@gmail.com',  # Replace with your own email address
            ['recipient@example.com'],  # Replace with the recipient's email address
            fail_silently=False,
        )

        # Redirect the user to a "thank you" page or any other desired page
        return HttpResponseRedirect(reverse('thank_you'))

    # Render the contact form template if it's a GET request
    return render(request, 'analysis/contact.html')


from django.shortcuts import render, redirect


def submit_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Perform any necessary form validation here
        
        # Example code to send an email
        send_mail(
            'Contact Form Submission',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            'shrestharajani155@gmail.com',  # Replace with your own email address
            ['recipient@example.com'],  # Replace with the recipient's email address
            fail_silently=False,
        )

        # Display a success message to the user
        messages.success(request, 'Thank you for contacting us!')

        # Redirect the user to a "thank you" page or any other desired page
        return redirect('thank_you')  # Replace 'thank_you' with the appropriate URL name

    return render(request, 'analysis/contact.html')  # Replace 'contact.html' with your contact form template


def thank_you(request):
    return render(request, 'analysis/thank_you.html')




