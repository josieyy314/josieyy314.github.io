install.packages("rlang",type="win.binary") 
#set working directory
setwd("C:/Users/wangw38/Desktop/info201/geog469/")


library("dplyr")


#install.packages("tidyr")
library("tidyr")

#get data
class_schedule <- read.csv('data/class_schedule.csv', stringsAsFactors = FALSE)

tag_table <- read.csv('data/tag_tableCSV.csv', stringsAsFactors = FALSE)
#new column (spacecode)

tags <- tag_table$TAGS

floor_num <- floor(class_schedule$Room_Number/100)

class_schedule <- mutate(class_schedule, space_code = (paste0(Building, "_", floor_num, "_", Room_Number)))

as.data.frame(tags) %>% separate(tags, into = paste("V", 1:9, sep = "_"))

#1. take building code, building 3 letters &  extract space code 
#write function that iterates through the string and checks for 
# is-numeric consecutive four times 
# underscore
# is-numeric again consceutive twice
# underscore
# then go until you hit a space
#2. clean up data so everything lines up, space code parts are V-6, V-7, V-8 
