import numpy as np
import matplotlib.dates as mdates
import subprocess
import matplotlib
import matplotlib.pyplot as plt
import time
import HTML

def create_total_dataset(path_to_archive,total_save_name,summary_name):
    """A function that reads all the data-files in 'path_to_archive' one by one,
    and saves them in one file called: 'total_save_name'"""
    print("Using create_total_dataset")
    bashCommand = "ls archive/" 
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    out = output.split()
    total_days = []
    num_records_per_day = []
    datalist_total = []
    for filename in out:
        print filename
        date =  filename[-14:-4] # in the format #YYYY-MM-DD
        total_days.append(date)
        #data = np.genfromtxt("archive/"+name,dtype=[('f0', 'S22'), ('f1', '<f8'), ('f2', '<f8'), ('f3', '<f8'), ('f4', '<f8'), ('f5', '<f8'), ('f6', '<f8'), ('f7', '<f8'), ('f8', '<f8')])
        #data = np.genfromtxt("archive/"+name,dtype=object)
        f = open(path_to_archive+filename,"r")
        linecount = 0
        for line in f:
            line = date + "--" + line 
            datalist_total.append(line)
            linecount = linecount + 1
        num_records_per_day.append(linecount)

    #---------Save 'total_save_name' - the main datafile
    f = open(total_save_name,"w")
    commentString = """#Description: Total Preliminary HPF Temperature Dataset \n#Date Sensor1 Sensor2 Sensor3 Sensor4 #Sensor5 Sensor6 Sensor7 Sensor8\n"""
    f.write(commentString)
    for writeline in datalist_total:
        f.write(writeline)
    f.close()
    #---------------------------------------------------

    #---------Save LakeShoreLogSummary.txt
    f = open(summary_name,"w")
    commentString = """#Description: HPF Temperature Dataset Summary \n#Showing the dates and corresponding number of records\n"""
    f.write(commentString)
    summary_string = ""
    for i in range(len(total_days)):
        summary_string = summary_string + str(i) + " " + total_days[i] + " " + str(num_records_per_day[i])+"\n"
    f.write(summary_string)
    f.close()
    pass

def read_total_dataset(total_save_name,numtime=1):
    """Read total_save_name, and returns a data construct with all the temperature data, and times, where 0 = NaN"""
    if numtime==1:
        data=np.genfromtxt(total_save_name,dtype=None,usemask=True,missing_values="0.0",converters={0:mdates.strpdate2num('%Y-%m-%d--%H:%M:%S')})
        data=data.filled(np.nan)
    else:
        data=np.genfromtxt(total_save_name,dtype=None,usemask=True,missing_values="0.0")
        data=data.filled(np.nan)
    #times=data['f0']
    return data

def read_summary(summary_name):
    """Reads and returns the data in the summary file (good for knowing the number of records per day)
    data['f0'] contains the date number
    data['f1'] contains the date
    data['f2'] contains the number of records for that date
    """
    return np.genfromtxt(summary_name,dtype=None)

def config_matplotlib():
    """Initialize matplotlib things: font size etc"""
    #------------Figure Layout--------------
    #---------------------FONT and other graphics------------------------
    font = {'family'         : 'serif',
            'size'	         : 10}
    matplotlib.rc('font',**font)
    matplotlib.rc('grid',linewidth=1)
    matplotlib.rc('xtick.major',width=2)
    matplotlib.rc('xtick.major',size=7)
    matplotlib.rc('xtick.minor',width=2)
    matplotlib.rc('xtick.minor',size=4)
    matplotlib.rc('ytick.major',width=2)
    matplotlib.rc('ytick.major',size=7)
    matplotlib.rc('ytick.minor',width=2)
    matplotlib.rc('ytick.minor',size=4)
    #-------------------------------------------------
    pass

def config_matplotlib_yale():
    """Initialize matplotlib things: font size etc"""
    #------------Figure Layout--------------
    #---------------------FONT and other graphics------------------------
    font = {'family'         : 'serif',
            'size'	         : 22} # for closeup
           # 'size'	         : 14} # for total dates
    matplotlib.rc('font',**font)
    matplotlib.rc('grid',linewidth=1)
    matplotlib.rc('xtick.major',width=2)
    matplotlib.rc('xtick.major',size=7)
    matplotlib.rc('xtick.minor',width=2)
    matplotlib.rc('xtick.minor',size=4)
    matplotlib.rc('ytick.major',width=2)
    matplotlib.rc('ytick.major',size=7)
    matplotlib.rc('ytick.minor',width=2)
    matplotlib.rc('ytick.minor',size=4)
    #-------------------------------------------------
    pass

def plot_all_dataset(total_save_name):
    """Plot all the dataset in LakeShoreLogTotal.txt"""
    #Read the data in LakeShoreLogTotal.txt
    data = read_total_dataset(total_save_name)

    #One Figure
    fig = plt.figure(dpi=40)
    ax = fig.add_subplot(111,title="HPF HET Temperature Monitoring")
    adjustprops = dict(left=0.19,bottom=0.15,right=0.92,top=0.9,wspace=0.,hspace=0.2)
    fig.subplots_adjust(**adjustprops)    

    ax.set_xlabel(r'Time (Timezone: UTC)',size="x-large")
    ax.set_ylabel(r'Temperature (C)',size="x-large")

    #ax.set_ylim(16.25,17.6)

    ax.minorticks_on()
    ax.grid()

    #PLOT
    ax.plot_date(x = data['f0'], y = data['f1'],fmt='r--',linewidth=1,label="#1 Cal-box Low")
    ax.plot_date(x = data['f0'], y = data['f2'],fmt='r-', linewidth=1,alpha=0.5,label="#2 Cal-box High")
    ax.plot_date(x = data['f0'], y = data['f3'],fmt='g--',linewidth=1,label="#3 Outside Low")
    ax.plot_date(x = data['f0'], y = data['f4'],fmt='g-' ,linewidth=1,alpha=0.5,label="#4 Outside High")
    ax.plot_date(x = data['f0'], y = data['f5'],fmt='b-' ,linewidth=1,alpha=0.5,label="#5 HPF-box High")
    ax.plot_date(x = data['f0'], y = data['f6'],fmt='b--',linewidth=1,label="#6 HPF-box Low")

    fig.autofmt_xdate()
    #ax.fmt_xdata = mdates.DateFormatter('%Y')

    ##-------------------------GRAPHICS---------------
    ax.legend(loc="lower center",prop={'size':7}, bbox_to_anchor=(0.5,1.05),fancybox=True,ncol=3)

    calc_stat_summary(data,"plots/"+total_save_name[:-4]+"_stats.txt")
    ##SAVING
    fig.savefig("plots/"+total_save_name[:-4]+".pdf",dpi=40)
    fig.savefig("plots/"+total_save_name[:-4]+".png",dpi=120)

    ##fig.show()
    pass

def plot_all_dataset_jan(total_save_name):
    """Plot all the dataset in LakeShoreLogTotal.txt from Jan 10th (first day in Jan with data) to present day"""
    #Read the data in LakeShoreLogTotal.txt

    jandate = '2015-01-10'
    today = time.strftime("%Y-%m-%d")
    #today = '2016-11-30'

    print("\nPlotting data from january 10, to " + today)
    try:
        plot_dates(total_save_name,jandate,today,outputname_single=True)
    except TypeError:
        print "Date " + today + " not in dataset! Try to rerun"
    ##fig.show()
    pass

def get_date_data(total_save_name,date1,date2=False):
    """Get and return the data between date1 and date2 (both included)"""

    summary_data = read_summary("LakeShoreLogSummary.txt")
    date_number = summary_data['f0']
    dates = summary_data['f1']
    records_per_date = summary_data['f2']

    #First if we have two dates given:
    if date2:
        num_date1 = date_number[dates==date1]
        num_date2 = date_number[dates==date2]
        req_data_start_index = sum(records_per_date[0:num_date1])
        req_data_end_index   = req_data_start_index + sum(records_per_date[num_date1:num_date2+1]) #+1 to include the latter one
        data_num_formatted = read_total_dataset(total_save_name,1)
        ##data_date_formatted = read_total_dataset(total_save_name,0)
        #data_length = len(data_date_formatted['f0'])
        #indices = np.zeros(data_length)
        #dates_stripped = data_date_formatted['f0']
        #for i in range(data_length):
        #    dates_stripped[i] = dates_stripped[i][-20:-10]
        data_requested = data_num_formatted[req_data_start_index:req_data_end_index]
        print("Length of data requested: ", len(data_requested))
        return data_requested
    #Or if we have only one date
    else:
        num_date = date_number[dates==date1]
        req_data_start_index = sum(records_per_date[0:num_date])
        req_data_end_index   = req_data_start_index + records_per_date[num_date] 
        data_num_formatted = read_total_dataset(total_save_name,1)
        data_requested = data_num_formatted[req_data_start_index:req_data_end_index]
        print("Length of data requested: ", len(data_requested))
        return data_requested

def plot_all_dataset_yale(total_save_name):
    """Plot all the dataset in LakeShoreLogTotal.txt"""
    #Read the data in LakeShoreLogTotal.txt
    data = read_total_dataset(total_save_name)

    #One Figure
    fig = plt.figure(dpi=40)
    ax = fig.add_subplot(111)#,title="HPF-HET Temperature Monitoring")
    adjustprops = dict(left=0.19,bottom=0.15,right=0.92,top=0.9,wspace=0.,hspace=0.2)
    fig.subplots_adjust(**adjustprops)    

    #ax.set_xlabel(r'Time',size="x-large")
    ax.set_ylabel(r'Temperature $(^{\circ}$C)',size="x-large")


    ax.minorticks_on()
    ax.grid()

    #PLOT
    #ax.plot_date(x = data['f0'], y = data['f1'],fmt='r--',linewidth=1,label="#1 Cal-box Low")
    #ax.plot_date(x = data['f0'], y = data['f2'],fmt='r-', linewidth=1,alpha=0.5,label="#2 Cal-box High")
    ax.plot_date(x = data['f0'], y = data['f3'],fmt='g--',linewidth=1,label="#3 Outside Low")
    ax.plot_date(x = data['f0'], y = data['f4'],fmt='g-' ,linewidth=1,alpha=0.4,label="#4 Outside High")
    ax.plot_date(x = data['f0'], y = data['f5'],fmt='b-' ,linewidth=1,alpha=0.5,label="#5 HPF-box High")
    ax.plot_date(x = data['f0'], y = data['f6'],fmt='b--',linewidth=1,label="#6 HPF-box Low")

    ax.set_ylim(15.25,18.5)
    fig.autofmt_xdate()
    #ax.fmt_xdata = mdates.DateFormatter('%Y')

    ##-------------------------GRAPHICS---------------
    ax.legend(loc="lower center",prop={'size':11}, bbox_to_anchor=(0.5,1.000),fancybox=True,ncol=2)

    calc_stat_summary(data,"plots/"+total_save_name[:-4]+"_stats.txt")
    ##SAVING
    fig.savefig("plots/"+total_save_name[:-4]+".pdf",dpi=40)
    fig.savefig("plots/"+total_save_name[:-4]+".png",dpi=120)

    ##fig.show()
    pass

def plot_dates(total_save_name,date1,date2=False,outputname_special=False,outputname_single=False):
    """Plot the temperature data for a given date: YYYY-MM-DD, and save to a file"""

    #Read the data in LakeShoreLogTotal.txt
    data = get_date_data(total_save_name,date1,date2)
    #If we have two dates given:
    if date2:
        date = date1 + "_to_" + date2
    else:
        date = date1

    #One Figure
    fig = plt.figure(dpi=40)
    ax = fig.add_subplot(111,title="HPF HET Temps for "+date)
    adjustprops = dict(left=0.19,bottom=0.15,right=0.92,top=0.9,wspace=0.,hspace=0.2)
    fig.subplots_adjust(**adjustprops)    

    ax.set_xlabel(r'Time (Timezone: UTC)',size="x-large")
    ax.set_ylabel(r'Temperature (C)',size="x-large")

    #ax.set_ylim(16.25,17.6)

    ax.minorticks_on()
    ax.grid()

    #PLOT
    ax.plot_date(x = data['f0'], y = data['f1'],fmt='r--',linewidth=1,label="#1 Cal-box Low")
    ax.plot_date(x = data['f0'], y = data['f2'],fmt='r-', linewidth=1,alpha=0.5,label="#2 Cal-box High")
    ax.plot_date(x = data['f0'], y = data['f3'],fmt='g--',linewidth=1,label="#3 Outside Low")
    ax.plot_date(x = data['f0'], y = data['f4'],fmt='g-' ,linewidth=1,alpha=0.5,label="#4 Outside High")
    ax.plot_date(x = data['f0'], y = data['f5'],fmt='b-' ,linewidth=1,alpha=0.5,label="#5 HPF-box High")
    ax.plot_date(x = data['f0'], y = data['f6'],fmt='b--',linewidth=1,label="#6 HPF-box Low")

    fig.autofmt_xdate()
    #ax.fmt_xdata = mdates.DateFormatter('%Y')

    ##-------------------------GRAPHICS---------------
    ax.legend(loc="lower center",prop={'size':7}, bbox_to_anchor=(0.5,1.05),fancybox=True,ncol=3)

    if outputname_special:
        ##Calculating summary data
        calc_stat_summary(data,"plots/"+total_save_name[:-4]+"_"+outputname_special+"_stats.txt")
        ##SAVING
        fig.savefig("plots/"+total_save_name[:-4]+"_"+outputname_special+".pdf",dpi=40)
        fig.savefig("plots/"+total_save_name[:-4]+"_"+outputname_special+".png",dpi=120)
    elif outputname_single:
        calc_stat_summary(data,"plots/"+total_save_name[:-4]+"_stats.txt")
        ##SAVING
        fig.savefig("plots/"+total_save_name[:-4]+".pdf",dpi=40)
        fig.savefig("plots/"+total_save_name[:-4]+".png",dpi=120)
    else:
        ##Calculating summary data
        calc_stat_summary(data,"plots/"+total_save_name[:-4]+"_"+date+"_stats.txt")
        ##SAVING
        fig.savefig("plots/"+total_save_name[:-4]+"_"+date+".pdf",dpi=40)
        fig.savefig("plots/"+total_save_name[:-4]+"_"+date+".png",dpi=120)
    ##fig.show()
    pass

def plot_dates_yale(total_save_name,date1,date2=False,outputname_special=False):
    """Plot the temperature data for a given date: YYYY-MM-DD, and save to a file"""

    #Read the data in LakeShoreLogTotal.txt
    data = get_date_data(total_save_name,date1,date2)
    #If we have two dates given:
    if date2:
        date = date1 + "_to_" + date2
    else:
        date = date1

    #One Figure
    fig = plt.figure(dpi=40)
    ax = fig.add_subplot(111)#,title="HPF HET Temps for "+date)
    adjustprops = dict(left=0.19,bottom=0.15,right=0.92,top=0.9,wspace=0.,hspace=0.2)
    fig.subplots_adjust(**adjustprops)    

    #ax.set_xlabel(r'Time (Timezone: UTC)',size="x-large")
    ax.set_ylabel(r'Temperature ($^{\circ}$C)',size="x-large")

    #ax.set_ylim(16.25,17.6)

    ax.minorticks_on()
    ax.grid()

    #PLOT
    #ax.plot_date(x = data['f0'], y = data['f1'],fmt='r--',linewidth=1,label="#1 Cal-box Low")
    #ax.plot_date(x = data['f0'], y = data['f2'],fmt='r-', linewidth=1,alpha=0.5,label="#2 Cal-box High")
    ax.plot_date(x = data['f0'], y = data['f3'],fmt='g--',linewidth=3,label="#3 Outside Low")
    ax.plot_date(x = data['f0'], y = data['f4'],fmt='g-' ,linewidth=3,alpha=0.4,label="#4 Outside High")
    ax.plot_date(x = data['f0'], y = data['f5'],fmt='b-' ,linewidth=3,alpha=0.5,label="#5 HPF-box High")
    ax.plot_date(x = data['f0'], y = data['f6'],fmt='b--',linewidth=3,label="#6 HPF-box Low")

    fig.autofmt_xdate()
    #ax.fmt_xdata = mdates.DateFormatter('%Y')

    ##-------------------------GRAPHICS---------------
    #ax.legend(loc="lower center",prop={'size':12}, bbox_to_anchor=(0.5,1.0),fancybox=True,ncol=2)

    if outputname_special:
        ##Calculating summary data
        calc_stat_summary(data,"plots/"+total_save_name[:-4]+"_"+outputname_special+"_stats.txt")
        ##SAVING
        fig.savefig("plots/"+total_save_name[:-4]+"_"+outputname_special+".pdf",dpi=40)
        fig.savefig("plots/"+total_save_name[:-4]+"_"+outputname_special+".png",dpi=120)
    else:
        ##Calculating summary data
        calc_stat_summary(data,"plots/"+total_save_name[:-4]+"_"+date+"_stats.txt")
        ##SAVING
        fig.savefig("plots/"+total_save_name[:-4]+"_"+date+".pdf",dpi=40)
        fig.savefig("plots/"+total_save_name[:-4]+"_"+date+".png",dpi=120)
    ##fig.show()
    pass

def plot_today(total_save_name):
    """Plot the temperature data for today (computer time)"""
    #Read the data in LakeShoreLogTotal.txt
    today = time.strftime("%Y-%m-%d")
    #today = '2016-11-30'
    print("\nPlotting data from today, " + today)
    try:
        plot_dates(total_save_name,today,outputname_special="today")
    except TypeError:
        print "Date " + today + " not in dataset! Try to rerun"


def plot_week(total_save_name):
    """Plots the last 7 days"""
    summary_data = read_summary('LakeShoreLogSummary.txt')
    date_number = summary_data['f0']
    dates = summary_data['f1']
    records_per_date = summary_data['f2']

    date1=dates[-7]
    date2=dates[-1]
    print("\nPlotting data from the last 7 days, from " + date1 + " to " + date2)
    try:
        plot_dates(total_save_name,date1,date2,outputname_special="week")
    except TypeError:
        print "Date " + date2 + " not in dataset! Try to rerun"

def plot_month(total_save_name):
    """Plots the last 7 days"""
    summary_data = read_summary('LakeShoreLogSummary.txt')
    date_number = summary_data['f0']
    dates = summary_data['f1']
    records_per_date = summary_data['f2']

    date1=dates[-30]
    date2=dates[-1]
    print("\nPlotting data from the last 30 days, from " + date1 + " to " + date2)
    try:
        plot_dates(total_save_name,date1,date2,outputname_special="month")
    except TypeError:
        print "Date " + date2 + " not in dataset! Try to rerun"

def calc_stat_summary(dataset,output_filename):
    """A program that calculates summary statistics for a given dataset and outputs it
    to the file 'output_filename'. Dataset is of the form data['f0'] etc."""

    d_mean  = np.zeros(7)
    d_std   = np.zeros(7)
    d_max   = np.zeros(7)
    d_min   = np.zeros(7)
    d_median= np.zeros(7)
    d_range = np.zeros(7)

    for i in range(7):
        d_mean[i]    = np.nanmean(dataset['f'+str(i)])
        d_std[i]     = np.nanstd(dataset['f'+str(i)])
        d_median[i]  = np.nanmedian(dataset['f'+str(i)])
        d_max[i]     = np.nanmax(dataset['f'+str(i)])
        d_min[i]     = np.nanmin(dataset['f'+str(i)])
        d_range[i]   = d_max[i] - d_min[i]

    #Saving results to file
    print("Saving results to file: " + output_filename)
    f = open(output_filename,"w")
    commentString = "#Summary Statistics for " + output_filename[:-4] + "\nSensor\tMean\tstd\tMedian\tMax\tMin\tRange\n"
    f.write(commentString)
    stat_str = ""
    sensors = ["Cal_Low","Cal_High","Out_Low","Out_High","HPF_High","HPF_Low"]
    for i in range(6):
        stat_str = stat_str + sensors[i] + "\t" + \
                num2str(d_mean[i+1],3) + "\t" + \
                num2str(d_std[i+1],3) + "\t" + \
                num2str(d_median[i+1],3) + "\t" + \
                num2str(d_max[i+1],3) + "\t" + \
                num2str(d_min[i+1],3) + "\t" + \
                num2str(d_range[i+1],3) + "\t" + \
                "\n"
    f.write(stat_str)
    f.close()
    #Also create html table
    txt2html(output_filename,output_filename[:-4]+".html")

def txt2html(input_filename,output_filename):
    """Read a txt file, called 'filename', and convert it to html table"""
    stat_data = np.genfromtxt(input_filename,dtype=None,comments="#")
    stat_data_list = stat_data.tolist()
    header_data = stat_data_list[0]
    table_data = stat_data_list[1:]
    htmlcode = HTML.table(table_data,header_row=header_data)
    f = open(output_filename,"w")
    f.write(htmlcode)
    f.close()
    print("Successfully converted "+input_filename+" to "+output_filename)

def num2str(num,precision):
    """docstring for num2str"""
    return "%0.*f" % (precision,num)

#def get_date_data(date,total_save_name):
#    """Get and return the data for a given date"""
#    data_num_formatted = read_total_dataset(total_save_name,1)
#    data_date_formatted = read_total_dataset(total_save_name,0)
#    data_length = len(data_date_formatted['f0'])
#    indices = np.zeros(data_length)
#    dates_stripped = data_date_formatted['f0']
#    for i in range(data_length):
#        dates_stripped[i] = dates_stripped[i][-20:-10]
#    
#    data_requested = data_num_formatted[dates_stripped==date]
#
#    print("Length of data requested: ", len(data_requested))
#
#    return data_requested
