import argparse, re
from halftone_lines import HalftoneLines

def str_to_rgb(str):
    '''
    Receives a string with a rgb value and returns a tuple with the 
    corresponding rgb value
    '''
    split = str[1:-1].split(",")
    return (int(split[0]), int(split[1]), int(split[2]))


def get_args():
    '''
    Reads and parses the arguments from the command line
    '''
    def rgb_color(arg, pat = re.compile("\([0-9]{1,3},[0-9]{1,3},[0-9]{1,3}\)")):
        arg = arg.replace(" ","")
        if( pat.match(arg) and
            int(arg[1:-1].split(",")[0]) < 256 and
            int(arg[1:-1].split(",")[1]) < 256 and
            int(arg[1:-1].split(",")[2]) < 256 ):
            return arg
        raise argparse.ArgumentTypeError("invalid rgb value")
    parser = argparse.ArgumentParser(description = "Generate halftone images w"+
    "ith lines")
    parser.add_argument("file", help = "(required)- String with the image name"+
    " (must include the image extension")
    parser.add_argument("-s", "--side", help = "(optional)- Length (in pixels)"+
    " of the side of each square that composes the output image (default is 20)"
    , type = int, default = 20)
    parser.add_argument("-k", "--kernel", help = "(optional)- Length (in pixel"+
    "s) of the side of each kernel (default is 0.7%% of the minimum between th"+
    "e width and height)", type = int, default = None)
    parser.add_argument("-bg", "--bg_color", help = "(optional)- Background co"+
    "lor of the output image in RGB (default is white)", default = "(255,255,2"+
    "55)", type = rgb_color)
    parser.add_argument("-fg", "--fg_color", help = "(optional)- Color of the "+
    "circles of the output image in RGB (default is black)", default = "(0,0,0)"
    , type = rgb_color)
    parser.add_argument("-al", "--alpha", help = "(optional)- Float (greater t"+
    "han 0) that controls the line's thickness (default is 1.2)", type = float, 
    default = 1.2)
    parser.add_argument("-an", "--angle", help = "(optional)- Float that deter"+
    "mines the orientation of the lines in the output image, in degrees (defau"+
    "lt is 20)", type = float, default = 20)
    parser.add_argument("-nv", "--no-verbose", help = "(optional)- Disables th"+
    "e printing of the progress message strings.", action = "store_false")
    parser.add_argument("-nc", "--no_contrast", help = "(optional)- Disables t"+
    "he application of the CLAHE histogram equalization algorithm that increas"+
    "es contrast.", action = "store_false")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    halftone = HalftoneLines(args.file, 
                            kernel_s    = args.kernel, 
                            side        = args.side, 
                            bg_color    = str_to_rgb(args.bg_color),
                            fg_color    = str_to_rgb(args.fg_color),
                            alpha       = args.alpha,
                            angle       = args.angle,
                            verbose     = args.no_verbose,
                            contrast    = args.no_contrast)
    halftone.halftone()
