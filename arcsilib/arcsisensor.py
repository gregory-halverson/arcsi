"""
Module that contains the ARCSIAbstractSensor class.
"""
############################################################################
#  arcsisensor.py
#
#  Copyright 2013 ARCSI.
#
#  ARCSI: 'Atmospheric and Radiometric Correction of Satellite Imagery'
#
#  ARCSI is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  ARCSI is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with ARCSI.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Purpose:  An abstract class which provides the base class for each
#           sensor supported by the ARCSI system.
#
# Author: Pete Bunting
# Email: pfb@aber.ac.uk
# Date: 05/07/2013
# Version: 1.0
#
# History:
# Version 1.0 - Created.
#
############################################################################

# Import the future functionality (for Python 2)
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
# import abstract base class stuff
from abc import ABCMeta, abstractmethod
# Import the datetime module
import datetime
# Import the ARCSI exception class
from .arcsiexception import ARCSIException
# Import the arcsi version number
from arcsilib import ARCSI_VERSION
# Import the arcsi copyright year
from arcsilib import ARCSI_COPYRIGHT_YEAR
# Import the arcsi support email
from arcsilib import ARCSI_SUPPORT_EMAIL
# Import the arcsi website
from arcsilib import ARCSI_WEBSITE
# Import the arcsi copyright names
from arcsilib import ARCSI_COPYRIGHT_NAMES
# Import the python collections library
import collections
# Import the python system library
import sys
# Import python math module
import math
# Import the rsgislib module
import rsgislib
# Import the rsgislib imagecalc module
import rsgislib.imagecalc
# Import the RSGISLib segmentation Module
import rsgislib.segmentation
# Import the RSGISLib Raster GIS Module
import rsgislib.rastergis
# Import the RSGISLib Image Utils Module
import rsgislib.imageutils
# Import the RSGISLib Image Calibration Module.
import rsgislib.imagecalibration
# Import the RSGISLib Elevation Module
import rsgislib.elevation
# Import the RSGISLib Image Filtering Module
import rsgislib.imagefilter
#Import the OSGEO GDAL module
import osgeo.gdal as gdal
# Import the osgeo ogr library
from osgeo import ogr
# Import the osgeo osr library
from osgeo import osr
# Import the ARCSI utilities class
from .arcsiutils import ARCSIUtils
# Import OS path module for manipulating the file system
import os.path
# Import the numpy module
import numpy
# Import the RIOS RAT library
from rios import rat
# Import the RIOS image reader
from rios.imagereader import ImageReader
# Import the RIOS image writer
from rios.imagewriter import ImageWriter
# Import the RBF interpolator from scipy
import scipy.interpolate.rbf
# Import scipy interpolation library
import scipy.interpolate
# Import JSON module
import json
# Import shutil module
import shutil

class ARCSIAbstractSensor (object):
    """
    An abstract class which represents a sensor and allows
    the various opperations required to be applied and standard
    variables (e.g., acqusiation date) stored and retrieved.
    """
    __metaclass__ = ABCMeta

    def __init__(self, debugMode, inputImage):
        self.sensor = "NA"
        self.userSpInputImage = inputImage
        self.debugMode = debugMode
        self.acquisitionTime = datetime.datetime.today()
        self.latTL = 0.0
        self.lonTL = 0.0
        self.latTR = 0.0
        self.lonTR = 0.0
        self.latBL = 0.0
        self.lonBL = 0.0
        self.latBR = 0.0
        self.lonBR = 0.0
        self.latCentre = 0.0
        self.lonCentre = 0.0
        self.xTL = 0.0
        self.yTL = 0.0
        self.xTR = 0.0
        self.yTR = 0.0
        self.xBL = 0.0
        self.yBL = 0.0
        self.xBR = 0.0
        self.yBR = 0.0
        self.xCentre = 0.0
        self.yCentre = 0.0
        self.inWKT = ""
        self.solarZenith = 0.0
        self.solarAzimuth = 0.0
        self.senorZenith = 0.0
        self.senorAzimuth = 0.0
        self.epsgCodes = dict()
        self.epsgCodes["WGS84UTM1N"] = 32601
        self.epsgCodes["WGS84UTM2N"] = 32602
        self.epsgCodes["WGS84UTM3N"] = 32603
        self.epsgCodes["WGS84UTM4N"] = 32604
        self.epsgCodes["WGS84UTM5N"] = 32605
        self.epsgCodes["WGS84UTM6N"] = 32606
        self.epsgCodes["WGS84UTM7N"] = 32607
        self.epsgCodes["WGS84UTM8N"] = 32608
        self.epsgCodes["WGS84UTM9N"] = 32609
        self.epsgCodes["WGS84UTM10N"] = 32610
        self.epsgCodes["WGS84UTM11N"] = 32611
        self.epsgCodes["WGS84UTM12N"] = 32612
        self.epsgCodes["WGS84UTM13N"] = 32613
        self.epsgCodes["WGS84UTM14N"] = 32614
        self.epsgCodes["WGS84UTM15N"] = 32615
        self.epsgCodes["WGS84UTM16N"] = 32616
        self.epsgCodes["WGS84UTM17N"] = 32617
        self.epsgCodes["WGS84UTM18N"] = 32618
        self.epsgCodes["WGS84UTM19N"] = 32619
        self.epsgCodes["WGS84UTM20N"] = 32620
        self.epsgCodes["WGS84UTM21N"] = 32621
        self.epsgCodes["WGS84UTM22N"] = 32622
        self.epsgCodes["WGS84UTM23N"] = 32623
        self.epsgCodes["WGS84UTM24N"] = 32624
        self.epsgCodes["WGS84UTM25N"] = 32625
        self.epsgCodes["WGS84UTM26N"] = 32626
        self.epsgCodes["WGS84UTM27N"] = 32627
        self.epsgCodes["WGS84UTM28N"] = 32628
        self.epsgCodes["WGS84UTM29N"] = 32629
        self.epsgCodes["WGS84UTM30N"] = 32630
        self.epsgCodes["WGS84UTM31N"] = 32631
        self.epsgCodes["WGS84UTM32N"] = 32632
        self.epsgCodes["WGS84UTM33N"] = 32633
        self.epsgCodes["WGS84UTM34N"] = 32634
        self.epsgCodes["WGS84UTM35N"] = 32635
        self.epsgCodes["WGS84UTM36N"] = 32636
        self.epsgCodes["WGS84UTM37N"] = 32637
        self.epsgCodes["WGS84UTM38N"] = 32638
        self.epsgCodes["WGS84UTM39N"] = 32639
        self.epsgCodes["WGS84UTM40N"] = 32640
        self.epsgCodes["WGS84UTM41N"] = 32641
        self.epsgCodes["WGS84UTM42N"] = 32642
        self.epsgCodes["WGS84UTM43N"] = 32643
        self.epsgCodes["WGS84UTM44N"] = 32644
        self.epsgCodes["WGS84UTM45N"] = 32645
        self.epsgCodes["WGS84UTM46N"] = 32646
        self.epsgCodes["WGS84UTM47N"] = 32647
        self.epsgCodes["WGS84UTM48N"] = 32648
        self.epsgCodes["WGS84UTM49N"] = 32649
        self.epsgCodes["WGS84UTM50N"] = 32650
        self.epsgCodes["WGS84UTM51N"] = 32651
        self.epsgCodes["WGS84UTM52N"] = 32652
        self.epsgCodes["WGS84UTM53N"] = 32653
        self.epsgCodes["WGS84UTM54N"] = 32654
        self.epsgCodes["WGS84UTM55N"] = 32655
        self.epsgCodes["WGS84UTM56N"] = 32656
        self.epsgCodes["WGS84UTM57N"] = 32657
        self.epsgCodes["WGS84UTM58N"] = 32658
        self.epsgCodes["WGS84UTM59N"] = 32659
        self.epsgCodes["WGS84UTM60N"] = 32660
        self.epsgCodes["WGS84UTM1S"] = 32701
        self.epsgCodes["WGS84UTM2S"] = 32702
        self.epsgCodes["WGS84UTM3S"] = 32703
        self.epsgCodes["WGS84UTM4S"] = 32704
        self.epsgCodes["WGS84UTM5S"] = 32705
        self.epsgCodes["WGS84UTM6S"] = 32706
        self.epsgCodes["WGS84UTM7S"] = 32707
        self.epsgCodes["WGS84UTM8S"] = 32708
        self.epsgCodes["WGS84UTM9S"] = 32709
        self.epsgCodes["WGS84UTM10S"] = 32710
        self.epsgCodes["WGS84UTM11S"] = 32711
        self.epsgCodes["WGS84UTM12S"] = 32712
        self.epsgCodes["WGS84UTM13S"] = 32713
        self.epsgCodes["WGS84UTM14S"] = 32714
        self.epsgCodes["WGS84UTM15S"] = 32715
        self.epsgCodes["WGS84UTM16S"] = 32716
        self.epsgCodes["WGS84UTM17S"] = 32717
        self.epsgCodes["WGS84UTM18S"] = 32718
        self.epsgCodes["WGS84UTM19S"] = 32719
        self.epsgCodes["WGS84UTM20S"] = 32720
        self.epsgCodes["WGS84UTM21S"] = 32721
        self.epsgCodes["WGS84UTM22S"] = 32722
        self.epsgCodes["WGS84UTM23S"] = 32723
        self.epsgCodes["WGS84UTM24S"] = 32724
        self.epsgCodes["WGS84UTM25S"] = 32725
        self.epsgCodes["WGS84UTM26S"] = 32726
        self.epsgCodes["WGS84UTM27S"] = 32727
        self.epsgCodes["WGS84UTM28S"] = 32728
        self.epsgCodes["WGS84UTM29S"] = 32729
        self.epsgCodes["WGS84UTM30S"] = 32730
        self.epsgCodes["WGS84UTM31S"] = 32731
        self.epsgCodes["WGS84UTM32S"] = 32732
        self.epsgCodes["WGS84UTM33S"] = 32733
        self.epsgCodes["WGS84UTM34S"] = 32734
        self.epsgCodes["WGS84UTM35S"] = 32735
        self.epsgCodes["WGS84UTM36S"] = 32736
        self.epsgCodes["WGS84UTM37S"] = 32737
        self.epsgCodes["WGS84UTM38S"] = 32738
        self.epsgCodes["WGS84UTM39S"] = 32739
        self.epsgCodes["WGS84UTM40S"] = 32740
        self.epsgCodes["WGS84UTM41S"] = 32741
        self.epsgCodes["WGS84UTM42S"] = 32742
        self.epsgCodes["WGS84UTM43S"] = 32743
        self.epsgCodes["WGS84UTM44S"] = 32744
        self.epsgCodes["WGS84UTM45S"] = 32745
        self.epsgCodes["WGS84UTM46S"] = 32746
        self.epsgCodes["WGS84UTM47S"] = 32747
        self.epsgCodes["WGS84UTM48S"] = 32748
        self.epsgCodes["WGS84UTM49S"] = 32749
        self.epsgCodes["WGS84UTM50S"] = 32750
        self.epsgCodes["WGS84UTM51S"] = 32751
        self.epsgCodes["WGS84UTM52S"] = 32752
        self.epsgCodes["WGS84UTM53S"] = 32753
        self.epsgCodes["WGS84UTM54S"] = 32754
        self.epsgCodes["WGS84UTM55S"] = 32755
        self.epsgCodes["WGS84UTM56S"] = 32756
        self.epsgCodes["WGS84UTM57S"] = 32757
        self.epsgCodes["WGS84UTM58S"] = 32758
        self.epsgCodes["WGS84UTM59S"] = 32759
        self.epsgCodes["WGS84UTM60S"] = 32760

    @abstractmethod
    def extractHeaderParameters(self, inputHeader, wktStr): pass

    def checkInputImageValid(self):
        if not self.expectedImageDataPresent():
            raise ARCSIException("Not all of the image(s) are present.")

    def defaultGenBaseOutFileName(self):
        """
        A function to generate a generic standard file
        base name which will be sensible.

        It is expected that individual sensors may override this function.
        """
        date = self.acquisitionTime.strftime("%Y%m%d")
        pos = "lat" + str(round(self.latCentre,)).replace('.', '').replace('-', '') + "lon" + str(round(self.lonCentre,2)).replace('.', '').replace('-', '')
        outname = self.sensor + "_" + date + "_" + pos
        return outname

    def generateOutputBaseName(self):
        """
        Provides a default implementation for generating file name.
        """
        return self.defaultGenBaseOutFileName()

    def getJSONDictDefaultMetaData(self, productsStr, validMaskImage="", footprintCalc=False, calcdValuesDict=dict(), outFilesDict=dict()):
        softwareDict = dict()
        softwareDict['Name'] = 'ARCSI'
        softwareDict['URL'] = ARCSI_WEBSITE
        softwareDict['Version'] = ARCSI_VERSION

        productsDict = dict()
        productsDict['ARCSIProducts'] = productsStr
        nowDateTime = datetime.datetime.today()
        processDateDict = dict()
        processDateDict['Year'] = nowDateTime.year
        processDateDict['Month'] = nowDateTime.month
        processDateDict['Day'] = nowDateTime.day
        productsDict['ProcessDate'] = processDateDict
        processTimeDict = dict()
        processTimeDict['Hour'] = nowDateTime.hour
        processTimeDict['Minute'] = nowDateTime.minute
        processTimeDict['Second'] = nowDateTime.second
        productsDict['ProcessTime'] = processTimeDict
        for key in calcdValuesDict:
            productsDict[key] = calcdValuesDict[key]

        filesDict = dict()
        filesDict['FileBaseName'] = self.generateOutputBaseName()
        for key in outFilesDict:
            filesDict[key] = os.path.basename(outFilesDict[key])

        sensorDict = dict()
        sensorDict['ARCSISensorName'] = self.sensor

        acqDict = dict()
        acqDateDict = dict()
        acqDateDict['Year'] = self.acquisitionTime.year
        acqDateDict['Month'] = self.acquisitionTime.month
        acqDateDict['Day'] = self.acquisitionTime.day
        acqDict['Date'] = acqDateDict
        acqTimeDict = dict()
        acqTimeDict['Hour'] = self.acquisitionTime.hour
        acqTimeDict['Minute'] = self.acquisitionTime.minute
        acqTimeDict['Second'] = self.acquisitionTime.second
        acqDict['Time'] = acqTimeDict
        acqDict['SolarZenith'] = self.solarZenith
        acqDict['SolarAzimuth'] = self.solarAzimuth
        acqDict['SenorZenith'] = self.senorZenith
        acqDict['SenorAzimuth'] = self.senorAzimuth

        locDict = dict()
        locGeogDict = dict()
        locGeogDict['CentreLon'] = self.lonCentre
        locGeogDict['CentreLat'] = self.latCentre
        locGeogBBOXDict = dict()
        locGeogBBOXDict['TLLat'] = self.latTL
        locGeogBBOXDict['TLLon'] = self.lonTL
        locGeogBBOXDict['TRLat'] = self.latTR
        locGeogBBOXDict['TRLon'] = self.lonTR
        locGeogBBOXDict['BLLat'] = self.latBL
        locGeogBBOXDict['BLLon'] = self.lonBL
        locGeogBBOXDict['BRLat'] = self.latBR
        locGeogBBOXDict['BRLon'] = self.lonBR
        locGeogDict['BBOX'] = locGeogBBOXDict
        locDict['Geographical'] = locGeogDict

        locProjDict = dict()
        if not validMaskImage is "":
            if not footprintCalc:
                rsgislib.rastergis.spatialExtent(clumps=validMaskImage, minXX='MinXX', minXY='MinXY', maxXX='MaxXX', maxXY='MaxXY', minYX='MinYX', minYY='MinYY', maxYX='MaxYX', maxYY='MaxYY', ratband=1)

            ratDataset = gdal.Open(validMaskImage)
            minXXVals = rat.readColumn(ratDataset, 'MinXX')
            minXYVals = rat.readColumn(ratDataset, 'MinXY')
            maxXXVals = rat.readColumn(ratDataset, 'MaxXX')
            maxXYVals = rat.readColumn(ratDataset, 'MaxXY')
            minYXVals = rat.readColumn(ratDataset, 'MinYX')
            minYYVals = rat.readColumn(ratDataset, 'MinYY')
            maxYXVals = rat.readColumn(ratDataset, 'MaxYX')
            maxYYVals = rat.readColumn(ratDataset, 'MaxYY')
            ratDataset = None

            ## Remove First Row which is no data...
            dataMask = numpy.ones_like(minXXVals, dtype=numpy.int16)
            dataMask[0] = 0
            minXXVals = minXXVals[dataMask == 1]
            minXYVals = minXYVals[dataMask == 1]
            maxXXVals = maxXXVals[dataMask == 1]
            maxXYVals = maxXYVals[dataMask == 1]
            minYXVals = minYXVals[dataMask == 1]
            minYYVals = minYYVals[dataMask == 1]
            maxYXVals = maxYXVals[dataMask == 1]
            maxYYVals = maxYYVals[dataMask == 1]

            ## Remove any features which are all zero (i.e., polygon not present...)
            minXXValsSub = minXXVals[numpy.logical_not((minXXVals == 0) & (minXYVals == 0) & (maxXXVals == 0) & (maxXYVals == 0) & (minYXVals == 0) & (minYYVals == 0) & (maxYXVals == 0) & (maxYYVals == 0))]
            minXYValsSub = minXYVals[numpy.logical_not((minXXVals == 0) & (minXYVals == 0) & (maxXXVals == 0) & (maxXYVals == 0) & (minYXVals == 0) & (minYYVals == 0) & (maxYXVals == 0) & (maxYYVals == 0))]
            maxXXValsSub = maxXXVals[numpy.logical_not((minXXVals == 0) & (minXYVals == 0) & (maxXXVals == 0) & (maxXYVals == 0) & (minYXVals == 0) & (minYYVals == 0) & (maxYXVals == 0) & (maxYYVals == 0))]
            maxXYValsSub = maxXYVals[numpy.logical_not((minXXVals == 0) & (minXYVals == 0) & (maxXXVals == 0) & (maxXYVals == 0) & (minYXVals == 0) & (minYYVals == 0) & (maxYXVals == 0) & (maxYYVals == 0))]
            minYXValsSub = minYXVals[numpy.logical_not((minXXVals == 0) & (minXYVals == 0) & (maxXXVals == 0) & (maxXYVals == 0) & (minYXVals == 0) & (minYYVals == 0) & (maxYXVals == 0) & (maxYYVals == 0))]
            minYYValsSub = minYYVals[numpy.logical_not((minXXVals == 0) & (minXYVals == 0) & (maxXXVals == 0) & (maxXYVals == 0) & (minYXVals == 0) & (minYYVals == 0) & (maxYXVals == 0) & (maxYYVals == 0))]
            maxYXValsSub = maxYXVals[numpy.logical_not((minXXVals == 0) & (minXYVals == 0) & (maxXXVals == 0) & (maxXYVals == 0) & (minYXVals == 0) & (minYYVals == 0) & (maxYXVals == 0) & (maxYYVals == 0))]
            maxYYValsSub = maxYYVals[numpy.logical_not((minXXVals == 0) & (minXYVals == 0) & (maxXXVals == 0) & (maxXYVals == 0) & (minYXVals == 0) & (minYYVals == 0) & (maxYXVals == 0) & (maxYYVals == 0))]

            numFeats = minXXValsSub.shape[0]

            if numFeats == 1:
                locProjBBOXDict = dict()
                locProjBBOXDict['TLX'] = minXXValsSub[0]
                locProjBBOXDict['TLY'] = maxYYValsSub[0]
                locProjBBOXDict['TRX'] = maxXXValsSub[0]
                locProjBBOXDict['TRY'] = maxYYValsSub[0]
                locProjBBOXDict['BLX'] = minXXValsSub[0]
                locProjBBOXDict['BLY'] = minYYValsSub[0]
                locProjBBOXDict['BRX'] = maxXXValsSub[0]
                locProjBBOXDict['BRY'] = minYYValsSub[0]
                locProjDict['BBOX'] = locProjBBOXDict
                locProjDict['CentreX'] = minXXValsSub[0] + ((maxXXValsSub[0] - minXXValsSub[0])/2)
                locProjDict['CentreY'] = minYYValsSub[0] + ((maxYYValsSub[0] - minYYValsSub[0])/2)

                locProjVPolyDict = dict()
                locProjVPolyDict['MinXX'] = minXXValsSub[0]
                locProjVPolyDict['MinXY'] = minXYValsSub[0]
                locProjVPolyDict['MaxYX'] = maxYXValsSub[0]
                locProjVPolyDict['MaxYY'] = maxYYValsSub[0]
                locProjVPolyDict['MaxXX'] = maxXXValsSub[0]
                locProjVPolyDict['MaxXY'] = maxXYValsSub[0]
                locProjVPolyDict['MinYX'] = minYXValsSub[0]
                locProjVPolyDict['MinYY'] = minYYValsSub[0]
                locProjDict['VPOLY'] = locProjVPolyDict
        else:
            locProjDict['CentreX'] = self.xCentre
            locProjDict['CentreY'] = self.yCentre
            locProjBBOXDict = dict()
            locProjBBOXDict['TLX'] = self.xTL
            locProjBBOXDict['TLY'] = self.yTL
            locProjBBOXDict['TRX'] = self.xTR
            locProjBBOXDict['TRY'] = self.yTR
            locProjBBOXDict['BLX'] = self.xBL
            locProjBBOXDict['BLY'] = self.yBL
            locProjBBOXDict['BRX'] = self.xBR
            locProjBBOXDict['BRY'] = self.yBR
            locProjDict['BBOX'] = locProjBBOXDict
        locDict['Projected'] = locProjDict

        jsonBlock = dict()
        jsonBlock['FileInfo'] = filesDict
        jsonBlock['SensorInfo'] = sensorDict
        jsonBlock['AcquasitionInfo'] = acqDict
        jsonBlock['LocationInfo'] = locDict
        jsonBlock['ProductsInfo'] = productsDict
        jsonBlock['SoftwareInfo'] = softwareDict

        return jsonBlock

    def generateMetaDataFile(self, outputPath, outputFileName, productsStr, validMaskImage="", footprintCalc=False, calcdValuesDict=dict(), outFilesDict=dict()):
        """
        Provides a default implementation for generating file metadata.
        """
        outJSONFilePath = os.path.join(outputPath, outputFileName)
        jsonData = self.getJSONDictDefaultMetaData(productsStr, validMaskImage, footprintCalc, calcdValuesDict, outFilesDict)
        with open(outJSONFilePath, 'w') as outfile:
            json.dump(jsonData, outfile, sort_keys=True,indent=4, separators=(',', ': '), ensure_ascii=False)

    @abstractmethod
    def expectedImageDataPresent(self): pass

    def maskInputImages(self):
        return False

    def imgNeedMosaicking(self):
        return False

    @abstractmethod
    def mosaicImageTiles(self): pass

    def hasThermal(self):
        return False

    def getReProjBBOX(self, wktFile, proj4File, useWKT2Reproject, xPxlRes, yPxlRes, snap2Grid):
        arcsiUtils = ARCSIUtils()
        projImgBBOX = dict()
        projImgBBOX['MinX'] = 0.0
        projImgBBOX['MaxX'] = 0.0
        projImgBBOX['MinY'] = 0.0
        projImgBBOX['MaxY'] = 0.0

        yPxlResAbs = math.fabs(yPxlRes)

        srcProj = osr.SpatialReference()
        srcProj.ImportFromWkt(self.inWKT)

        tarProj = osr.SpatialReference()
        if useWKT2Reproject:
            wktStr = arcsiUtils.readTextFile(wktFile)
            tarProj.ImportFromWkt(wktStr)
        else:
            proj4Str = arcsiUtils.readTextFile(proj4File)
            tarProj.ImportFromProj4(proj4Str)

        wktPt = 'POINT(%s %s)' % (self.xTL, self.yTL)
        point = ogr.CreateGeometryFromWkt(wktPt)
        point.AssignSpatialReference(srcProj)
        point.TransformTo(tarProj)

        print("Pxl Res: [{0}, {1} ({2})]".format(xPxlRes, yPxlRes, yPxlResAbs))

        minXPt = (math.floor(point.GetX()/xPxlRes)*xPxlRes)
        maxYPt = (math.ceil(point.GetY()/yPxlResAbs)*yPxlResAbs)

        projImgBBOX['MinX'] = minXPt
        projImgBBOX['MaxY'] = maxYPt

        print("MinX: [{0}, {1}]".format(point.GetX(), minXPt))
        print("MaxY: [{0}, {1}]".format(point.GetY(), maxYPt))

        wktPt = 'POINT(%s %s)' % (self.xBR, self.yBR)
        point = ogr.CreateGeometryFromWkt(wktPt)
        point.AssignSpatialReference(srcProj)
        point.TransformTo(tarProj)

        maxXPt = (math.ceil(point.GetX()/xPxlRes)*xPxlRes)
        minYPt = (math.floor(point.GetY()/yPxlResAbs)*yPxlResAbs)

        projImgBBOX['MaxX'] = maxXPt
        projImgBBOX['MinY'] = minYPt

        print("MaxX: [{0}, {1}]".format(point.GetX(), maxXPt))
        print("MinY: [{0}, {1}]".format(point.GetY(), minYPt))

        return projImgBBOX


    @abstractmethod
    def applyImageDataMask(self, inputHeader, outputPath, outputMaskName, outputImgName, outFormat, outWKTFile): pass

    @abstractmethod
    def convertImageToRadiance(self, outputPath, outputReflName, outputThermalName, outFormat): pass

    @abstractmethod
    def generateImageSaturationMask(self, outputPath, outputName, outFormat): pass

    def generateValidImageDataMask(self, outputPath, outputMaskName, viewAngleImg, outFormat):
        return None

    def generateImageFootprint(self, validMaskImage, outputPath, outputName):
        print("Creating Vector Footprint...")
        rsgislib.rastergis.spatialExtent(clumps=validMaskImage, minXX='MinXX', minXY='MinXY', maxXX='MaxXX', maxXY='MaxXY', minYX='MinYX', minYY='MinYY', maxYX='MaxYX', maxYY='MaxYY', ratband=1)
        ratDataset = gdal.Open(validMaskImage)

        minXXVals = rat.readColumn(ratDataset, 'MinXX')
        minXYVals = rat.readColumn(ratDataset, 'MinXY')
        maxXXVals = rat.readColumn(ratDataset, 'MaxXX')
        maxXYVals = rat.readColumn(ratDataset, 'MaxXY')
        minYXVals = rat.readColumn(ratDataset, 'MinYX')
        minYYVals = rat.readColumn(ratDataset, 'MinYY')
        maxYXVals = rat.readColumn(ratDataset, 'MaxYX')
        maxYYVals = rat.readColumn(ratDataset, 'MaxYY')

        ## Remove First Row which is no data...
        dataMask = numpy.ones_like(minXXVals, dtype=numpy.int16)
        dataMask[0] = 0
        minXXVals = minXXVals[dataMask == 1]
        minXYVals = minXYVals[dataMask == 1]
        maxXXVals = maxXXVals[dataMask == 1]
        maxXYVals = maxXYVals[dataMask == 1]
        minYXVals = minYXVals[dataMask == 1]
        minYYVals = minYYVals[dataMask == 1]
        maxYXVals = maxYXVals[dataMask == 1]
        maxYYVals = maxYYVals[dataMask == 1]

        ## Remove any features which are all zero (i.e., polygon not present...)
        minXXValsSub = minXXVals[numpy.logical_not((minXXVals == 0) & (minXYVals == 0) & (maxXXVals == 0) & (maxXYVals == 0) & (minYXVals == 0) & (minYYVals == 0) & (maxYXVals == 0) & (maxYYVals == 0))]
        minXYValsSub = minXYVals[numpy.logical_not((minXXVals == 0) & (minXYVals == 0) & (maxXXVals == 0) & (maxXYVals == 0) & (minYXVals == 0) & (minYYVals == 0) & (maxYXVals == 0) & (maxYYVals == 0))]
        maxXXValsSub = maxXXVals[numpy.logical_not((minXXVals == 0) & (minXYVals == 0) & (maxXXVals == 0) & (maxXYVals == 0) & (minYXVals == 0) & (minYYVals == 0) & (maxYXVals == 0) & (maxYYVals == 0))]
        maxXYValsSub = maxXYVals[numpy.logical_not((minXXVals == 0) & (minXYVals == 0) & (maxXXVals == 0) & (maxXYVals == 0) & (minYXVals == 0) & (minYYVals == 0) & (maxYXVals == 0) & (maxYYVals == 0))]
        minYXValsSub = minYXVals[numpy.logical_not((minXXVals == 0) & (minXYVals == 0) & (maxXXVals == 0) & (maxXYVals == 0) & (minYXVals == 0) & (minYYVals == 0) & (maxYXVals == 0) & (maxYYVals == 0))]
        minYYValsSub = minYYVals[numpy.logical_not((minXXVals == 0) & (minXYVals == 0) & (maxXXVals == 0) & (maxXYVals == 0) & (minYXVals == 0) & (minYYVals == 0) & (maxYXVals == 0) & (maxYYVals == 0))]
        maxYXValsSub = maxYXVals[numpy.logical_not((minXXVals == 0) & (minXYVals == 0) & (maxXXVals == 0) & (maxXYVals == 0) & (minYXVals == 0) & (minYYVals == 0) & (maxYXVals == 0) & (maxYYVals == 0))]
        maxYYValsSub = maxYYVals[numpy.logical_not((minXXVals == 0) & (minXYVals == 0) & (maxXXVals == 0) & (maxXYVals == 0) & (minYXVals == 0) & (minYYVals == 0) & (maxYXVals == 0) & (maxYYVals == 0))]

        numFeats = minXXValsSub.shape[0]

        outShpLayerNamePath = os.path.join(outputPath, outputName)
        driver = ogr.GetDriverByName("ESRI Shapefile")
        if os.path.exists(outShpLayerNamePath+".shp"):
            driver.DeleteDataSource(outShpLayerNamePath+".shp")
        outDatasource = driver.CreateDataSource(outShpLayerNamePath+ ".shp")
        raster_srs = osr.SpatialReference()
        raster_srs.ImportFromWkt(ratDataset.GetProjectionRef())
        outLayer = outDatasource.CreateLayer(outShpLayerNamePath, srs=raster_srs) #ratDataset.GetProjection()

        fieldYearDefn = ogr.FieldDefn('Year', ogr.OFTInteger)
        fieldYearDefn.SetWidth(6)
        outLayer.CreateField(fieldYearDefn)

        fieldMonthDefn = ogr.FieldDefn('Month', ogr.OFTInteger)
        fieldMonthDefn.SetWidth(6)
        outLayer.CreateField(fieldMonthDefn)

        fieldDayDefn = ogr.FieldDefn('Day', ogr.OFTInteger)
        fieldDayDefn.SetWidth(6)
        outLayer.CreateField(fieldDayDefn)

        fieldBaseNameDefn = ogr.FieldDefn('BaseName', ogr.OFTString)
        fieldBaseNameDefn.SetWidth(254)
        outLayer.CreateField(fieldBaseNameDefn)

        fieldSolZenDefn = ogr.FieldDefn('SolZen', ogr.OFTReal)
        fieldSolZenDefn.SetWidth(10)
        fieldSolZenDefn.SetPrecision(6)
        outLayer.CreateField(fieldSolZenDefn)

        fieldSolAziDefn = ogr.FieldDefn('SolAzi', ogr.OFTReal)
        fieldSolAziDefn.SetWidth(10)
        fieldSolAziDefn.SetPrecision(6)
        outLayer.CreateField(fieldSolAziDefn)

        fieldSenZenDefn = ogr.FieldDefn('SenZen', ogr.OFTReal)
        fieldSenZenDefn.SetWidth(10)
        fieldSenZenDefn.SetPrecision(6)
        outLayer.CreateField(fieldSenZenDefn)

        fieldSenAziDefn = ogr.FieldDefn('SenAzi', ogr.OFTReal)
        fieldSenAziDefn.SetWidth(10)
        fieldSenAziDefn.SetPrecision(6)
        outLayer.CreateField(fieldSenAziDefn)

        fieldCenLatDefn = ogr.FieldDefn('CenLat', ogr.OFTReal)
        fieldCenLatDefn.SetWidth(10)
        fieldCenLatDefn.SetPrecision(6)
        outLayer.CreateField(fieldCenLatDefn)

        fieldCenLonDefn = ogr.FieldDefn('CenLon', ogr.OFTReal)
        fieldCenLonDefn.SetWidth(10)
        fieldCenLonDefn.SetPrecision(6)
        outLayer.CreateField(fieldCenLonDefn)

        print("Create and Add Polygons...")
        for i in range(numFeats):
            wktStr = "POLYGON((" + str(minXXValsSub[i]) + " " + str(minXYValsSub[i]) + ", " + str(maxYXValsSub[i]) + " " + str(maxYYValsSub[i]) + ", " + str(maxXXValsSub[i]) + " " + str(maxXYValsSub[i]) + ", " + str(minYXValsSub[i]) + " " + str(minYYValsSub[i]) + ", " + str(minXXValsSub[i]) + " " + str(minXYValsSub[i]) + "))"
            #print(str(i) + ": " + wktStr)
            poly = ogr.CreateGeometryFromWkt(wktStr)
            feat = ogr.Feature( outLayer.GetLayerDefn())
            feat.SetGeometry(poly)
            #print(
            feat.SetField("Year", self.acquisitionTime.year)
            feat.SetField("Month", self.acquisitionTime.month)
            feat.SetField("Day", self.acquisitionTime.day)
            feat.SetField("BaseName", self.generateOutputBaseName())
            feat.SetField("SolZen", self.solarZenith)
            feat.SetField("SolAzi", self.solarAzimuth)
            feat.SetField("SenZen", self.senorZenith)
            feat.SetField("SenAzi", self.senorAzimuth)
            feat.SetField("CenLat", self.latCentre)
            feat.SetField("CenLon", self.lonCentre)

            if outLayer.CreateFeature(feat) != 0:
                print(str(i) + ": " + wktStr)
                print("Failed to create feature in shapefile.\n")
                sys.exit( 1 )
            feat.Destroy()

        outDatasource.Destroy()
        ratDataset = None

    def generateTopoDirectShadowMask(self,  inputDEMImage, outputPath, outputName, outFormat, tmpPath):
        try:
            print("Calculating a direct topographic shadow mask.")
            print("Solar Zenith = " + str(self.solarZenith) + " Solar Azimuth = " + str(self.solarAzimuth))
            arcsiUtils = ARCSIUtils()
            outputImage = os.path.join(outputPath, outputName)
            tmpBaseName = os.path.splitext(outputName)[0]
            imgExtension = arcsiUtils.getFileExtension(outFormat)
            outputTmpFile = os.path.join(tmpPath, tmpBaseName + "_toposhadow_tmp" + imgExtension)

            demDataset = gdal.Open( inputDEMImage, gdal.GA_ReadOnly )
            if demDataset is None:
                raise ARCSIException("Could not open DEM dataset.")
            demBand = demDataset.GetRasterBand(1)
            demMax = demBand.GetMaximum()
            if demMax is None:
                (demMin,demMax) = band.ComputeRasterMinMax(0)
            rsgislib.elevation.shadowmask(inputDEMImage, outputTmpFile, self.solarAzimuth, self.solarZenith, demMax, outFormat)
            rsgislib.imagefilter.applyMedianFilter(outputTmpFile, outputImage, 3, outFormat, rsgislib.TYPE_8UINT)

            if not self.debugMode:
                gdalDriver = gdal.GetDriverByName(outFormat)
                gdalDriver.Delete(outputTmpFile)

            return outputImage
        except Exception as e:
            raise e

    @abstractmethod
    def convertThermalToBrightness(self, inputRadImage, outputPath, outputName, outFormat, scaleFactor): pass

    @abstractmethod
    def convertImageToTOARefl(self, inputRadImage, outputPath, outputName, outFormat, scaleFactor): pass

    @abstractmethod
    def generateCloudMask(self, inputReflImage, inputSatImage, inputThermalImage, inputValidImg, outputPath, outputName, outFormat, tmpPath, scaleFactor): pass

    def generateClearSkyMask(self, cloudsImg, inputValidImg, outputPath, outputName, outFormat, tmpPath,  initClearSkyRegionDist=3000, initClearSkyRegionMinSize=3000, finalClearSkyRegionDist=1000, morphSize=21):
        try:
            arcsiUtils = ARCSIUtils()
            outputImage = os.path.join(outputPath, outputName)
            tmpBaseName = os.path.splitext(outputName)[0]
            imgExtension = arcsiUtils.getFileExtension(outFormat)
            tmpBaseDIR = os.path.join(tmpPath, tmpBaseName)

            tmpDIRExisted = True
            if not os.path.exists(tmpBaseDIR):
                os.makedirs(tmpBaseDIR)
                tmpDIRExisted = False

            deleteTmpFiles = not self.debugMode

            rsgislib.imagecalibration.calcClearSkyRegions(cloudsImg, inputValidImg, outputImage, outFormat, tmpBaseDIR, deleteTmpFiles, initClearSkyRegionDist, initClearSkyRegionMinSize, finalClearSkyRegionDist, morphSize)

            if not self.debugMode:
                if not tmpDIRExisted:
                    shutil.rmtree(tmpBaseDIR, ignore_errors=True)

            return outputImage
        except Exception as e:
            raise e


    @abstractmethod
    def convertImageToSurfaceReflSglParam(self, inputRadImage, outputPath, outputName, outFormat, aeroProfile, atmosProfile, grdRefl, surfaceAltitude, aotVal, useBRDF, scaleFactor): pass

    @abstractmethod
    def calc6SCoefficients(self, aeroProfile, atmosProfile, grdRefl, surfaceAltitude, aotVal): pass

    def buildElevation6SCoeffLUT(self, aeroProfile, atmosProfile, grdRefl, aotVal, useBRDF, surfaceAltitudeMin, surfaceAltitudeMax):
        elevLUTFeat = collections.namedtuple('ElevLUTFeat', ['Elev', 'Coeffs'])
        lut = list()
        elevRange = (surfaceAltitudeMax - surfaceAltitudeMin) / 100
        numElevSteps = int(math.ceil(elevRange) + 1)
        elevVal = surfaceAltitudeMin
        for i in range(numElevSteps):
            print("Building LUT Elevation ", elevVal)
            lut.append(elevLUTFeat(Elev=elevVal, Coeffs=self.calc6SCoefficients(aeroProfile, atmosProfile, grdRefl, (float(elevVal)/1000), aotVal, useBRDF)))
            elevVal = elevVal + 100
        return lut

    @abstractmethod
    def convertImageToSurfaceReflDEMElevLUT(self, inputRadImage, inputDEMFile, outputPath, outputName, outFormat, aeroProfile, atmosProfile, grdRefl, aotVal, useBRDF, surfaceAltitudeMin, surfaceAltitudeMax, scaleFactor, elevCoeffs=None): pass

    def buildElevationAOT6SCoeffLUT(self, aeroProfile, atmosProfile, grdRefl, useBRDF, surfaceAltitudeMin, surfaceAltitudeMax, aotMin, aotMax):
        elevLUTFeat = collections.namedtuple('ElevLUTFeat', ['Elev', 'Coeffs'])
        aotLUTFeat = collections.namedtuple('AOTLUTFeat', ['AOT', 'Coeffs'])
        lut = list()
        elevRange = (surfaceAltitudeMax - surfaceAltitudeMin) / 100
        numElevSteps = int(math.ceil(elevRange) + 1)
        elevVal = surfaceAltitudeMin

        aotRange = (aotMax - aotMin) / 0.05
        numAOTSteps = int(math.ceil(aotRange) + 1) + 1
        aotVal = aotMin

        for i in range(numElevSteps):
            print("Building LUT Elevation ", elevVal)
            aotVal = aotMin
            aotCoeffLUT = list()
            for j in range(numAOTSteps):
                aotCoeffLUT.append(aotLUTFeat(AOT=aotVal,  Coeffs=self.calc6SCoefficients(aeroProfile, atmosProfile, grdRefl, (float(elevVal)/1000), aotVal, useBRDF)))
                aotVal = aotVal + 0.05
            lut.append(elevLUTFeat(Elev=elevVal, Coeffs=aotCoeffLUT))
            elevVal = elevVal + 100
        return lut

    @abstractmethod
    def convertImageToSurfaceReflAOTDEMElevLUT(self, inputRadImage, inputDEMFile, inputAOTImage, outputPath, outputName, outFormat, aeroProfile, atmosProfile, grdRefl, useBRDF, surfaceAltitudeMin, surfaceAltitudeMax, aotMin, aotMax, scaleFactor, elevAOTCoeffs=None): pass

    def calcDarkTargetOffsetsForBand(self, inputTOAImage, offsetImage, band, outFormat, histBinWidth, minObjSize, darkPxlPercentile, tmpDarkPxlsImg, tmpDarkPxlsClumpsImg, tmpDarkPxlsClumpsRMSmallImg, tmpDarkObjsImg):
        print("Band: ", band)
        bandHist = rsgislib.imagecalc.getHistogram(inputTOAImage, band, histBinWidth, False, 1, 10000)
        #print(bandHist)
        sumPxls = numpy.sum(bandHist[0])
        #print("Total Num Pixels: ", sumPxls)
        findTargets = True

        while findTargets:
            findTargets = False
            numPxlThreshold = sumPxls * darkPxlPercentile #0.001 # 1th percentile
            #print("Number of pixels = ", numPxlThreshold)

            pxlThreshold = 0
            pxlCount = 0
            for bin in bandHist[0]:
                pxlCount = pxlCount + bin
                if pxlCount < numPxlThreshold:
                    pxlThreshold = pxlThreshold + histBinWidth
                else:
                    break
            print("Image Band Threshold (For Dark Pixels) = ", pxlThreshold)

            dataType = rsgislib.TYPE_8UINT
            expression = str('(b1!=0)&&(b1<=') + str(pxlThreshold) + str(')?1:0')
            bandDefns = []
            bandDefns.append(rsgislib.imagecalc.BandDefn('b1', inputTOAImage, band))
            rsgislib.imagecalc.bandMath(tmpDarkPxlsImg, expression, outFormat, dataType, bandDefns)
            rsgislib.segmentation.clump(tmpDarkPxlsImg, tmpDarkPxlsClumpsImg, outFormat, False, 0.0)
            rsgislib.rastergis.populateStats(tmpDarkPxlsClumpsImg, True, False)
            rsgislib.segmentation.rmSmallClumps(tmpDarkPxlsClumpsImg, tmpDarkPxlsClumpsRMSmallImg, minObjSize, outFormat)
            rsgislib.segmentation.relabelClumps(tmpDarkPxlsClumpsRMSmallImg, tmpDarkObjsImg, outFormat, False)
            rsgislib.rastergis.populateStats(tmpDarkObjsImg, True, False)
            stats2CalcTOA = list()
            stats2CalcTOA.append(rsgislib.rastergis.BandAttStats(band=(band), minField="MinTOARefl", meanField="MeanTOARefl"))
            rsgislib.rastergis.populateRATWithStats(inputTOAImage, tmpDarkObjsImg, stats2CalcTOA)

            ratDS = gdal.Open(tmpDarkObjsImg, gdal.GA_Update)
            Histogram = rat.readColumn(ratDS, "Histogram")
            if Histogram.size > 10:
                findTargets = False
                ratDS = None
                break
            else:
                findTargets = True
                darkPxlPercentile = darkPxlPercentile * 2
                print("Trying Dark Pixel Percentile Threshold: " + str(darkPxlPercentile))
                ratDS = None

        ratDS = gdal.Open(tmpDarkObjsImg, gdal.GA_Update)
        Histogram = rat.readColumn(ratDS, "Histogram")
        selected = Histogram * 2
        selected[...] = 1
        selected[0] = 0
        rat.writeColumn(ratDS, "Selected", selected)
        ratDS = None

        rsgislib.rastergis.spatialLocation(tmpDarkObjsImg, "Eastings", "Northings")
        rsgislib.rastergis.selectClumpsOnGrid(tmpDarkObjsImg, "Selected", "SelectedGrid", "Eastings", "Northings", "MeanTOARefl", "min", 20, 20)

        ratDS = gdal.Open(tmpDarkObjsImg, gdal.GA_Update)
        Eastings = rat.readColumn(ratDS, "Eastings")
        Northings = rat.readColumn(ratDS, "Northings")
        MinTOARefl = rat.readColumn(ratDS, "MinTOARefl")
        SelectedGrid = rat.readColumn(ratDS, "SelectedGrid")
        ratDS = None

        Eastings = Eastings[SelectedGrid!=0]
        Northings = Northings[SelectedGrid!=0]
        MinTOARefl = MinTOARefl[SelectedGrid!=0]

        interpSmoothing = 10.0
        self.interpolateImageFromPointData(inputTOAImage, Eastings, Northings, MinTOARefl, offsetImage, outFormat, interpSmoothing, True, 0.0)

    def findPerBandDarkTargetsOffsets(self, inputTOAImage, numBands, outputPath, outputName, outFormat, tmpPath, minObjSize, darkPxlPercentile):
        try:
            arcsiUtils = ARCSIUtils()
            tmpBaseName = os.path.splitext(outputName)[0]
            binWidth = 1

            bandDarkTargetOffsetImages = list()
            imgExtension = arcsiUtils.getFileExtension(outFormat)
            tmpDarkPxlsImg = os.path.join(tmpPath, tmpBaseName + "_darkpxls" + imgExtension)
            tmpDarkPxlsClumpsImg = os.path.join(tmpPath, tmpBaseName + "_darkclumps" + imgExtension)
            tmpDarkPxlsClumpsRMSmallImg = os.path.join(tmpPath, tmpBaseName + "_darkclumpsrmsmall" + imgExtension)
            tmpDarkObjsImg = os.path.join(tmpPath, tmpBaseName+"_darkobjs"+imgExtension)

            for band in range(numBands):
                offsetImage = os.path.join(tmpPath, tmpBaseName+"_darktargetoffs_b"+str(band+1)+imgExtension)
                self.calcDarkTargetOffsetsForBand(inputTOAImage, offsetImage, band+1, outFormat, binWidth, minObjSize, darkPxlPercentile, tmpDarkPxlsImg, tmpDarkPxlsClumpsImg, tmpDarkPxlsClumpsRMSmallImg, tmpDarkObjsImg)
                bandDarkTargetOffsetImages.append(offsetImage)

            outputImage = os.path.join(outputPath, tmpBaseName + "_dosuboffs" + imgExtension)
            print(outputImage)
            rsgislib.imageutils.stackImageBands(bandDarkTargetOffsetImages, None, outputImage, None, 0, outFormat, rsgislib.TYPE_32FLOAT)

            if not self.debugMode:
                gdalDriver = gdal.GetDriverByName(outFormat)
                gdalDriver.Delete(tmpDarkPxlsImg)
                gdalDriver.Delete(tmpDarkPxlsClumpsImg)
                gdalDriver.Delete(tmpDarkPxlsClumpsRMSmallImg)
                gdalDriver.Delete(tmpDarkObjsImg)
                for image in bandDarkTargetOffsetImages:
                    gdalDriver.Delete(image)

            return outputImage

        except Exception as e:
            raise e

    def performDOSOnSingleBand(self, inputTOAImage, band, outputPath, tmpBaseName, bandName, outFormat, tmpPath, minObjSize, darkPxlPercentile, dosOutRefl):
        try:
            arcsiUtils = ARCSIUtils()
            binWidth = 1

            imgExtension = arcsiUtils.getFileExtension(outFormat)
            tmpDarkPxlsImg = os.path.join(tmpPath, tmpBaseName + "_darkpxls" + imgExtension)
            tmpDarkPxlsClumpsImg = os.path.join(tmpPath, tmpBaseName + "_darkclumps" + imgExtension)
            tmpDarkPxlsClumpsRMSmallImg = os.path.join(tmpPath, tmpBaseName + "_darkclumpsrmsmall" + imgExtension)
            tmpDarkObjsImg = os.path.join(tmpPath, tmpBaseName+"_darkobjs"+imgExtension)

            offsetImage = os.path.join(outputPath, tmpBaseName+"_darktargetoffs_b"+str(band)+imgExtension)
            self.calcDarkTargetOffsetsForBand(inputTOAImage, offsetImage, band, outFormat, binWidth, minObjSize, darkPxlPercentile, tmpDarkPxlsImg, tmpDarkPxlsClumpsImg, tmpDarkPxlsClumpsRMSmallImg, tmpDarkObjsImg)

            outputName = tmpBaseName + "DOS" + bandName + imgExtension
            outputImage = os.path.join(outputPath, outputName)
            print(outputImage)

            bandDefns = []
            bandDefns.append(rsgislib.imagecalc.BandDefn('Off', offsetImage, 1))
            bandDefns.append(rsgislib.imagecalc.BandDefn('TOA', inputTOAImage, band))
            expression = '(TOA==0)?0:((TOA-Off)+' + str(dosOutRefl) + ')<=0?1.0:(TOA-Off)+' + str(dosOutRefl)
            rsgislib.imagecalc.bandMath(outputImage, expression, outFormat, rsgislib.TYPE_16UINT, bandDefns)

            if not self.debugMode:
                gdalDriver = gdal.GetDriverByName(outFormat)
                gdalDriver.Delete(tmpDarkPxlsImg)
                gdalDriver.Delete(tmpDarkPxlsClumpsImg)
                gdalDriver.Delete(tmpDarkPxlsClumpsRMSmallImg)
                gdalDriver.Delete(tmpDarkObjsImg)

            return outputImage

        except Exception as e:
            raise e

    def performLocalDOSOnSingleBand(self, inputTOAImage, band, outputPath, tmpBaseName, bandName, outFormat, tmpPath, minObjSize, darkPxlPercentile, blockSize, dosOutRefl):
        try:
            arcsiUtils = ARCSIUtils()
            bandDarkTargetOffsetImages = list()
            imgExtension = arcsiUtils.getFileExtension(outFormat)
            tmpDarkTargetAllImage = os.path.join(tmpPath, tmpBaseName + "_darkpxls_allbands" + imgExtension)
            tmpDarkPxlsImg = os.path.join(tmpPath, tmpBaseName + "_darkpxls" + imgExtension)
            tmpDarkPxlsClumpsImg = os.path.join(tmpPath, tmpBaseName + "_darkclumps" + imgExtension)
            tmpDarkPxlsClumpsRMSmallImg = os.path.join(tmpPath, tmpBaseName + "_darkclumpsrmsmall" + imgExtension)
            tmpDarkObjsImg = os.path.join(tmpPath, tmpBaseName+"_darkobjs"+imgExtension)

            binWidth = 1
            self.findDOSLocalDarkTargets(inputTOAImage, tmpDarkTargetAllImage, blockSize, "KEA", binWidth, darkPxlPercentile)

            print("Band ", band)
            rsgislib.imageutils.selectImageBands(tmpDarkTargetAllImage, tmpDarkPxlsImg, "KEA", rsgislib.TYPE_8UINT, [band])
            rsgislib.segmentation.clump(tmpDarkPxlsImg, tmpDarkPxlsClumpsImg, "KEA", False, 0.0)
            rsgislib.rastergis.populateStats(tmpDarkPxlsClumpsImg, True, False)
            rsgislib.segmentation.rmSmallClumps(tmpDarkPxlsClumpsImg, tmpDarkPxlsClumpsRMSmallImg, minObjSize, "KEA")
            rsgislib.segmentation.relabelClumps(tmpDarkPxlsClumpsRMSmallImg, tmpDarkObjsImg, "KEA", False)
            rsgislib.rastergis.populateStats(tmpDarkObjsImg, True, False)
            stats2CalcTOA = list()
            stats2CalcTOA.append(rsgislib.rastergis.BandAttStats(band=(band+1), minField="MinTOARefl", meanField="MeanTOARefl"))
            rsgislib.rastergis.populateRATWithStats(inputTOAImage, tmpDarkObjsImg, stats2CalcTOA)

            ratDS = gdal.Open(tmpDarkObjsImg, gdal.GA_Update)
            Histogram = rat.readColumn(ratDS, "Histogram")
            selected = Histogram * 2
            selected[...] = 1
            selected[0] = 0
            rat.writeColumn(ratDS, "Selected", selected)
            ratDS = None

            rsgislib.rastergis.spatialLocation(tmpDarkObjsImg, "Eastings", "Northings")
            rsgislib.rastergis.selectClumpsOnGrid(tmpDarkObjsImg, "Selected", "SelectedGrid", "Eastings", "Northings", "MeanTOARefl", "min", 20, 20)

            print("Interpolating the offset image...")

            offsetImage = os.path.join(tmpPath, tmpBaseName+"_darktargetoffs_b"+str(band)+imgExtension)

            ratDS = gdal.Open(tmpDarkObjsImg, gdal.GA_Update)
            Eastings = rat.readColumn(ratDS, "Eastings")
            Northings = rat.readColumn(ratDS, "Northings")
            MinTOARefl = rat.readColumn(ratDS, "MinTOARefl")
            SelectedGrid = rat.readColumn(ratDS, "SelectedGrid")
            ratDS = None

            Eastings = Eastings[SelectedGrid!=0]
            Northings = Northings[SelectedGrid!=0]
            MinTOARefl = MinTOARefl[SelectedGrid!=0]

            interpSmoothing = 10.0
            self.interpolateImageFromPointData(inputTOAImage, Eastings, Northings, MinTOARefl, offsetImage, "KEA", interpSmoothing, True, 0.0)

            outputName = tmpBaseName + "DOS" + bandName + imgExtension
            outputImage = os.path.join(outputPath, outputName)
            print(outputImage)

            bandDefns = []
            bandDefns.append(rsgislib.imagecalc.BandDefn('Off', offsetImage, 1))
            bandDefns.append(rsgislib.imagecalc.BandDefn('TOA', inputTOAImage, band))
            expression = '(TOA==0)?0:((TOA-Off)+' + str(dosOutRefl) + ')<=0?1.0:(TOA-Off)+' + str(dosOutRefl)
            rsgislib.imagecalc.bandMath(outputImage, expression, outFormat, rsgislib.TYPE_16UINT, bandDefns)

            if not self.debugMode:
                gdalDriver = gdal.GetDriverByName("KEA")
                gdalDriver.Delete(tmpDarkPxlsImg)
                gdalDriver.Delete(tmpDarkPxlsClumpsImg)
                gdalDriver.Delete(tmpDarkPxlsClumpsRMSmallImg)
                gdalDriver.Delete(tmpDarkObjsImg)
                gdalDriver.Delete(tmpDarkTargetAllImage)
                gdalDriver.Delete(offsetImage)

            return outputImage

        except Exception as e:
            raise e

    def findDOSLocalDarkTargets(self, inputTOAImage, darkTargetImage, blockSize, outFormat, histBinWidth, darkPxlPercentile):
        reader = ImageReader(inputTOAImage, windowxsize=blockSize, windowysize=blockSize)
        writer = None
        for (info, block) in reader:
            out = numpy.zeros_like(block)

            # Iterate through the image bands
            for i in range(len(out)):
                minVal = numpy.min(block[i])
                maxVal = numpy.max(block[i])
                #print("Band: ", i+1, " Min = ", minVal, " Max = ", maxVal)
                if ((maxVal - minVal) > 5):
                    data = block[i].flatten()
                    data = data[data != 0]

                    minVal = numpy.min(data)
                    maxVal = numpy.max(data)

                    numBins = (math.ceil(maxVal - minVal) / histBinWidth) + 1
                    if data.shape[0] > ((blockSize*blockSize)*0.1):
                        #out[i,...] = 1
                        histo, histoBins = numpy.histogram(data, bins=numBins, range=(float(minVal), float(maxVal)))
                        numValues = numpy.sum(histo)
                        numValsPercentile = math.floor(numValues * darkPxlPercentile)
                        #print("Num Values: ", numValues, " percentile: ", numValsPercentile)
                        #print("Histo: ", histo)
                        #print("Bins: ", histoBins)
                        binValCount = 0
                        threshold = 0.0
                        for n in range(histo.shape[0]):
                            if (binValCount + histo[n]) > numValsPercentile:
                                break
                            else:
                                binValCount =  binValCount + histo[n]
                                threshold = histoBins[n+1]
                        #print("Threshold = ", threshold)
                        out[i, ((block[i] <= threshold) & (block[i] > 0))] = 1
                    else:
                        out[i,...] = 0

            if writer is None:
                writer = ImageWriter(darkTargetImage,
                                     info=info,
                                     firstblock=out,
                                     drivername=outFormat,
                                     creationoptions=[])
            else:
                writer.write(out)
        writer.close(calcStats=False)

    def findPerBandLocalDarkTargetsOffsets(self, inputTOAImage, numBands, outputPath, outputName, outFormat, tmpPath, blockSize, minObjSize, darkPxlPercentile):
        try:
            arcsiUtils = ARCSIUtils()
            tmpBaseName = os.path.splitext(outputName)[0]
            binWidth = 1

            bandDarkTargetOffsetImages = list()
            imgExtension = arcsiUtils.getFileExtension(outFormat)
            tmpDarkTargetAllImage = os.path.join(tmpPath, tmpBaseName + "_darkpxls_allbands" + imgExtension)
            tmpDarkPxlsImg = os.path.join(tmpPath, tmpBaseName + "_darkpxls" + imgExtension)
            tmpDarkPxlsClumpsImg = os.path.join(tmpPath, tmpBaseName + "_darkclumps" + imgExtension)
            tmpDarkPxlsClumpsRMSmallImg = os.path.join(tmpPath, tmpBaseName + "_darkclumpsrmsmall" + imgExtension)
            tmpDarkObjsImg = os.path.join(tmpPath, tmpBaseName+"_darkobjs"+imgExtension)

            self.findDOSLocalDarkTargets(inputTOAImage, tmpDarkTargetAllImage, blockSize, outFormat, binWidth, darkPxlPercentile)

            for band in range(numBands):
                print("Band ", band+1)
                rsgislib.imageutils.selectImageBands(tmpDarkTargetAllImage, tmpDarkPxlsImg, outFormat, rsgislib.TYPE_8UINT, [band+1])
                rsgislib.segmentation.clump(tmpDarkPxlsImg, tmpDarkPxlsClumpsImg, outFormat, False, 0.0)
                rsgislib.rastergis.populateStats(tmpDarkPxlsClumpsImg, True, False)
                rsgislib.segmentation.rmSmallClumps(tmpDarkPxlsClumpsImg, tmpDarkPxlsClumpsRMSmallImg, minObjSize, outFormat)
                rsgislib.segmentation.relabelClumps(tmpDarkPxlsClumpsRMSmallImg, tmpDarkObjsImg, outFormat, False)
                rsgislib.rastergis.populateStats(tmpDarkObjsImg, True, False)
                stats2CalcTOA = list()
                stats2CalcTOA.append(rsgislib.rastergis.BandAttStats(band=(band+1), minField="MinTOARefl", meanField="MeanTOARefl"))
                rsgislib.rastergis.populateRATWithStats(inputTOAImage, tmpDarkObjsImg, stats2CalcTOA)

                ratDS = gdal.Open(tmpDarkObjsImg, gdal.GA_Update)
                Histogram = rat.readColumn(ratDS, "Histogram")
                selected = Histogram * 2
                selected[...] = 1
                selected[0] = 0
                rat.writeColumn(ratDS, "Selected", selected)
                ratDS = None

                rsgislib.rastergis.spatialLocation(tmpDarkObjsImg, "Eastings", "Northings")
                rsgislib.rastergis.selectClumpsOnGrid(tmpDarkObjsImg, "Selected", "SelectedGrid", "Eastings", "Northings", "MeanTOARefl", "min", 20, 20)

                print("Interpolating the offset image...")

                offsetImage = os.path.join(tmpPath, tmpBaseName+"_darktargetoffs_b"+str(band+1)+imgExtension)

                ratDS = gdal.Open(tmpDarkObjsImg, gdal.GA_Update)
                Eastings = rat.readColumn(ratDS, "Eastings")
                Northings = rat.readColumn(ratDS, "Northings")
                MinTOARefl = rat.readColumn(ratDS, "MinTOARefl")
                SelectedGrid = rat.readColumn(ratDS, "SelectedGrid")
                ratDS = None

                Eastings = Eastings[SelectedGrid!=0]
                Northings = Northings[SelectedGrid!=0]
                MinTOARefl = MinTOARefl[SelectedGrid!=0]

                interpSmoothing = 10.0
                self.interpolateImageFromPointData(inputTOAImage, Eastings, Northings, MinTOARefl, offsetImage, outFormat, interpSmoothing, True, 0.0)

                bandDarkTargetOffsetImages.append(offsetImage)

            outputImage = os.path.join(outputPath, tmpBaseName + "_dosuboffs" + imgExtension)
            print(outputImage)
            rsgislib.imageutils.stackImageBands(bandDarkTargetOffsetImages, None, outputImage, None, 0, outFormat, rsgislib.TYPE_32FLOAT)

            if not self.debugMode:
                gdalDriver = gdal.GetDriverByName(outFormat)
                gdalDriver.Delete(tmpDarkPxlsImg)
                gdalDriver.Delete(tmpDarkPxlsClumpsImg)
                gdalDriver.Delete(tmpDarkPxlsClumpsRMSmallImg)
                gdalDriver.Delete(tmpDarkObjsImg)
                gdalDriver.Delete(tmpDarkTargetAllImage)
                for image in bandDarkTargetOffsetImages:
                    gdalDriver.Delete(image)

            return outputImage

        except Exception as e:
            raise e

    def convertImageToReflectanceSimpleDarkSubtract(self, inputTOAImage, outputPath, outputName, outFormat, dosOutRefl, offsetsList=None):
        try:
            print("Perform Simple Dark Object Subtraction")
            outputImage = os.path.join(outputPath, outputName)

            if offsetsList is None:
                percentiles = rsgislib.imagecalc.bandPercentile(inputTOAImage, 0.01, 0)
                offsetsList = list()
                OffVal = collections.namedtuple('DOSOffset', ['offset'])
                for val in percentiles:
                    offsetsList.append(OffVal(offset=val))

            rsgislib.imagecalibration.applySubtractSingleOffsets(inputTOAImage, outputImage, outFormat, rsgislib.TYPE_16UINT, True, True, 0.0, dosOutRefl, offsetsList)

            return outputImage, offsetsList
        except Exception as e:
            raise e

    def convertImageBandToReflectanceSimpleDarkSubtract(self, inputTOAImage, outputPath, outputName, outFormat, dosOutRefl, imgBand):
        try:
            print("Perform Simple Dark Object Subtraction on image band")
            outputImage = os.path.join(outputPath, outputName)

            percentiles = rsgislib.imagecalc.bandPercentile(inputTOAImage, 0.01, 0)

            print("Band offset = " + str(percentiles[imgBand-1]))
            expression = "(b1 == 0.0)?0.0:((b1-" + str(percentiles[imgBand-1]) + ") + " + str(dosOutRefl) + ") < 0?1.0: (b1-" + str(percentiles[imgBand-1]) + ") + " + str(dosOutRefl)
            bandDefns = []
            bandDefns.append(rsgislib.imagecalc.BandDefn('b1', inputTOAImage, imgBand))
            rsgislib.imagecalc.bandMath(outputImage, expression, outFormat, rsgislib.TYPE_16UINT, bandDefns)

            return outputImage, percentiles[imgBand-1]
        except Exception as e:
            raise e

    @abstractmethod
    def convertImageToReflectanceDarkSubstract(self, inputTOAImage, outputPath, outputName, outFormat, tmpPath, globalDOS, dosOutRefl, offsetsImage=None): pass

    @abstractmethod
    def findDDVTargets(self, inputTOAImage, outputPath, outputName, outFormat, tmpPath): pass

    @abstractmethod
    def estimateImageToAODUsingDDV(self, inputRADImage, inputTOAImage, inputDEMFile, shadowMask, outputPath, outputName, outFormat, tmpPath, aeroProfile, atmosProfile, grdRefl, aotValMin, aotValMax): pass

    @abstractmethod
    def estimateImageToAODUsingDOS(self, inputRADImage, inputTOAImage, inputDEMFile, shadowMask, outputPath, outputName, outFormat, tmpPath, aeroProfile, atmosProfile, grdRefl, aotValMin, aotValMax, globalDOS, simpleDOS, dosOutRefl): pass

    @abstractmethod
    def estimateSingleAOTFromDOS(self, radianceImage, toaImage, inputDEMFile, tmpPath, outputName, outFormat, aeroProfile, atmosProfile, grdRefl, minAOT, maxAOT, dosOutRefl): pass

    def estimateSingleAOTFromDOSBandImpl(self, radianceImage, toaImage, inputDEMFile, tmpPath, outputName, outFormat, aeroProfile, atmosProfile, grdRefl, aotValMin, aotValMax, dosOutRefl, imgBand):
        try:
            print("Estimating a single AOD value Using DOS")
            # Using a simple DOS find RAD and SREF a value from within the image.
            radVal = 0.0
            srefVal = 0.0
            arcsiUtils = ARCSIUtils()
            dosBandFileName = outputName + "_simbanddos"+ arcsiUtils.getFileExtension(outFormat)
            dosBandFile, bandOff = self.convertImageBandToReflectanceSimpleDarkSubtract(toaImage, tmpPath, dosBandFileName, outFormat, dosOutRefl, imgBand)

            darkROIMask = os.path.join(tmpPath, outputName + "_darkROIMask"+ arcsiUtils.getFileExtension(outFormat))
            expression = "((b1 != 0) && (b1 < " + str(dosOutRefl+5) + "))?1.0:0.0"
            bandDefns = []
            bandDefns.append(rsgislib.imagecalc.BandDefn('b1', dosBandFile, 1))
            rsgislib.imagecalc.bandMath(darkROIMask, expression, outFormat, rsgislib.TYPE_8UINT, bandDefns)

            darkROIMaskClumps = os.path.join(tmpPath, outputName + "_darkROIMaskClumps"+ arcsiUtils.getFileExtension(outFormat))
            rsgislib.segmentation.clump(darkROIMask, darkROIMaskClumps, outFormat, False, 0.0)
            rsgislib.rastergis.populateStats(darkROIMaskClumps, True, False)

            darkROIMaskClumpsRMSmall = os.path.join(tmpPath, outputName + "_darkROIMaskClumpsRMSmall"+ arcsiUtils.getFileExtension(outFormat))
            rsgislib.segmentation.rmSmallClumps(darkROIMaskClumps, darkROIMaskClumpsRMSmall, 5, outFormat)
            darkROIMaskClumpsFinal = os.path.join(tmpPath, outputName + "_darkROIMaskClumpsFinal"+ arcsiUtils.getFileExtension(outFormat))
            rsgislib.segmentation.relabelClumps(darkROIMaskClumpsRMSmall, darkROIMaskClumpsFinal, outFormat, False)
            rsgislib.rastergis.populateStats(darkROIMaskClumpsFinal, True, False)

            stats2CalcDOS = list()
            stats2CalcDOS.append(rsgislib.rastergis.BandAttStats(band=imgBand, meanField="MeanTOARefl"))
            rsgislib.rastergis.populateRATWithStats(toaImage, darkROIMaskClumpsFinal, stats2CalcDOS)
            stats2CalcRAD = list()
            stats2CalcRAD.append(rsgislib.rastergis.BandAttStats(band=imgBand, meanField="MeanRad"))
            rsgislib.rastergis.populateRATWithStats(radianceImage, darkROIMaskClumpsFinal, stats2CalcRAD)
            stats2CalcElev = list()
            stats2CalcElev.append(rsgislib.rastergis.BandAttStats(band=1, meanField="MeanElev"))
            rsgislib.rastergis.populateRATWithStats(inputDEMFile, darkROIMaskClumpsFinal, stats2CalcElev)


            ratDS = gdal.Open(darkROIMaskClumpsFinal, gdal.GA_ReadOnly)
            Histogram = rat.readColumn(ratDS, "Histogram")
            MeanTOARefl = rat.readColumn(ratDS, "MeanTOARefl")
            MeanRad = rat.readColumn(ratDS, "MeanRad")
            MeanElev = rat.readColumn(ratDS, "MeanElev")
            ratDS = None

            maxObjSizeArrIdx = numpy.where(Histogram == numpy.max(Histogram))

            #print("maxObjSizeArrIdx = ", maxObjSizeArrIdx[0][0])

            reflTOA = MeanTOARefl[maxObjSizeArrIdx][0]
            reflDOS = reflTOA - bandOff
            if reflDOS < dosOutRefl:
                reflDOS = dosOutRefl
            reflDOS = reflDOS/1000
            radVal = MeanRad[maxObjSizeArrIdx][0]
            elevVal = MeanElev[maxObjSizeArrIdx][0]

            #print("reflTOA = ", reflTOA)
            #print("reflDOS = ", reflDOS)
            #print("radVal = ", radVal)
            #print("elevVal = ", elevVal)

            if not self.debugMode:
                gdalDriver = gdal.GetDriverByName(outFormat)
                gdalDriver.Delete(dosBandFile)
                gdalDriver.Delete(darkROIMask)
                gdalDriver.Delete(darkROIMaskClumps)
                gdalDriver.Delete(darkROIMaskClumpsRMSmall)
                gdalDriver.Delete(darkROIMaskClumpsFinal)

            # Second Step - estimate AOT to get RAD value to SREF.
            numAOTValTests = int(math.ceil((aotValMax - aotValMin)/0.05))+1
            if not numAOTValTests >= 1:
                raise ARCSIException("min and max AOT range are too close together, they need to be at least 0.05 apart.")

            cAOT = aotValMin
            cDist = 0.0
            minAOT = 0.0
            minDist = 0.0

            for j in range(numAOTValTests):
                cAOT = aotValMin + (0.05 * j)
                cDist = self.run6SToOptimiseAODValue(cAOT, radVal, reflDOS, aeroProfile, atmosProfile, grdRefl, elevVal/1000)
                if j == 0:
                    minAOT = cAOT
                    minDist = cDist
                elif cDist < minDist:
                    minAOT = cAOT
                    minDist = cDist
            aotVal = minAOT
            print("IDENTIFIED AOT: ", aotVal)

            return aotVal
        except Exception as e:
            raise

    @abstractmethod
    def setBandNames(self, imageFile): pass

#    def interpolateImageFromPointData(self, templateInImage, xVals, yVals, zVals, outputImage, outFormat, smoothingParam, notNegOut, notNegMinVal):
#        print("Interpolating Image: Number of Features = ", xVals.shape[0])
#        rbfi = scipy.interpolate.rbf.Rbf(xVals, yVals, zVals, function='linear', smooth=smoothingParam)
#
#        reader = ImageReader(templateInImage, windowxsize=200, windowysize=200)
#        writer = None
#        for (info, block) in reader:
#            pxlCoords = info.getBlockCoordArrays()
#            interZ = rbfi(pxlCoords[0].flatten(), pxlCoords[1].flatten())
#            if notNegOut:
#                interZ = numpy.where(interZ < 0, notNegMinVal, interZ)
#            out = numpy.reshape(interZ, block[0].shape)
#            out = numpy.expand_dims(out, axis=0)
#
#            if writer is None:
#                writer = ImageWriter(outputImage,
#                                     info=info,
#                                     firstblock=out,
#                                     drivername=outFormat,
#                                     creationoptions=[])
#            else:
#                writer.write(out)
#        writer.close(calcStats=True)
#        print("Interpolating Image - Complete")


    def interpolateImageFromPointData(self, templateInImage, xVals, yVals, zVals, outputImage, outFormat, smoothingParam, notNegOut, notNegMinVal):
        print("Interpolating Image: Number of Features = ", xVals.shape[0])

        reader = ImageReader(templateInImage, windowxsize=200, windowysize=200)
        writer = None
        for (info, block) in reader:
            pxlCoords = info.getBlockCoordArrays()
            interZnn = scipy.interpolate.griddata((xVals, yVals), zVals, (pxlCoords[0].flatten(), pxlCoords[1].flatten()), method='nearest')
            interZcub = scipy.interpolate.griddata((xVals, yVals), zVals, (pxlCoords[0].flatten(), pxlCoords[1].flatten()), method='cubic')
            interZ = numpy.where(numpy.isnan(interZcub), interZnn, interZcub)
            if notNegOut:
                interZ = numpy.where(interZ < 0, notNegMinVal, interZ)
            out = numpy.reshape(interZ, block[0].shape)
            out = numpy.expand_dims(out, axis=0)

            if writer is None:
                writer = ImageWriter(outputImage,
                                     info=info,
                                     firstblock=out,
                                     drivername=outFormat,
                                     creationoptions=[])
            else:
                writer.write(out)
        writer.close(calcStats=True)
        print("Interpolating Image - Complete")

    def cleanFollowProcessing(self):
        print("")


