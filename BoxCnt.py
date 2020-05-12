import imagej
import csv
def DimensionCalculator(url):
    dimension = 0
    ij = imagej.init('./Imagej/Fiji.app', headless=False)  # Start ImageJ from local file

    image = ij.io().open(url)
    ij.ui().show(image)
    macro = """
        run("8-bit");
        setAutoThreshold("Default dark");
        //run("Threshold...");
        //setThreshold(128, 255);
        setAutoThreshold("Default dark");
        setOption("BlackBackground", true);
        run("Convert to Mask", "method=Default background=Dark calculate black");
        run("Fractal Box Count...", "box=2,3,4,6,8,12,16,32,64");
        saveAs("Results","./Results/ResultsBC.csv");
        run("Close")
        run("Close")
        run("Close")
        """
    ij.py.run_macro(macro)

    # reading results from saved csv file
    with open('./Results/ResultsBC.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                dimension = row[10]
                line_count += 1
    #print(f'Dimension is {dimension}, source image: {url}')
    return dimension

if __name__ == '__main__':
    #urls = 'C:/Users/JakubZ/Documents/Škola/VŠ/Bakalárska práca/obrazky/aea1c36752535785aaedd91e84c357ca.jpg'
    #urls = 'https://i.pinimg.com/originals/ae/a1/c3/aea1c36752535785aaedd91e84c357ca.jpg'
    urls = 'C:/Users/JakubZ/Documents/Škola/VŠ/Bakalárska práca/obrazky/vonKochSnowflake.PNG'

    print (f'Dimension is {DimensionCalculator(urls)}, source image: {urls}.')