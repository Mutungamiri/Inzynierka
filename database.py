import MySQLdb
import matplotlib.pyplot as plt
import pandas
import seaborn as sns

def rysuj():
    print("Wybierz czujnik")
    i = input()
    conn = MySQLdb.connect(host="localhost", user="root", passwd="test", db="System_alarmowy")
    query = """SELECT data_czas, stan_czujnika FROM Pomiary_Czujniki WHERE ID_czujnika =""" + str(i)
    df = pandas.read_sql(query, conn)
    fig, ax = plt.subplots()
    fig = sns.barplot(x="data_czas", y="stan_czujnika", data=df, estimator=sum,
    ci = None, ax = ax, color = ’blue’)
    x_dates = df[’data_czas’].dt.strftime(’%Y-%m-%d %H:%M:%S’).sort_values().unique()
    ax.set_xticklabels(labels=x_dates, rotation=15, ha=’right’)
    plt.xlabel(’Czas’)
    plt.ylabel(’Stan czujnika’)
    plt.title(’Czujnik nr ’ + i)
    plt.show()
    conn.close()
    menu()
def menu():
    operacja = input(’’’
    Wybierz opcje
    [1] Generuj wykres
    [2] Wyjdz
    ’’’)
    if operacja == ’1’:
    rysuj()
    elif operacja == ’2’:
    print(’Dowidzenia’)
menu()