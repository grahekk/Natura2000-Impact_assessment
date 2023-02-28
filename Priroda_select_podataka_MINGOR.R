library(readxl)
library(dplyr)
library(tidyr)
library(stringr)
library(purrr)
library(readr)
library(data.table)
library(zoo)
library(tidyverse)
library(plyr)

rm(list=ls())
Popis_strogo_zasticenih_vrsta <- read_excel("~/Rstudio/Popis strogo zasticenih vrsta.xlsx")

#the data to be checked
e <- environment()
pat_staza <- c("S:/1_PUOP/1_SPUO/SPUO_III_Iid_Medjimurske_zupanije/2_Radno/1_priroda/Nikola/data_export/")
list.files(path = pat_staza, pattern = ".csv") -> ls_names
str_c(pat_staza, list.files(path = pat_staza, pattern = ".csv")) -> ls_paths
#load of data
map(setNames(ls_paths, ls_names), read_csv) %>% as.environment() -> e
#e %>% as.list %>% rbindlist(fill = T, idcol = T) -> e_s
e %>% ldply() -> e_s
e_s %>% mutate(source = .id, .keep = "unused") -> e_s

#now the list of usual names of variables i want to check if they exist and select them
imena_atributa <- c("IMENALAT", "Vrst", "Naziv", "Ime", "validno", "latin", "znan", "svojt", "source")
Imena_izbac <- c("Prez", "Proj", "Obj", "Hrv", "opa", "trac", "tran", "lo", "GPS", "pr_1", "determ", "1", "IDVRSTE")
e_s %>% colnames

#wrangle of the data
e_s %>% 
  select(contains(imena_atributa)) %>% 
  select(-contains(Imena_izbac)) %>% 
  mutate(najvalidnije = ifelse(is.na(Validno_im), Ime_svojte, Validno_im), .keep = "unused", merged = NA, ime_svojte = NULL, Validno_im = NULL) -> eselec
eselec %>% unite("merged", -source, na.rm = T, sep = " ") %>% unique -> eselec

eselec %>% 
  select(merged) %>% 
  unlist %>% 
  word(start = 1L, end = 2L) %>% 
  as.character() -> eselec$merged

#the last part, comparing it with the official data and joining
#wrangling of this data
Strogozv <- Popis_strogo_zasticenih_vrsta
Popis_strogo_zasticenih_vrsta %>% 
  select(`VRSTA - znanstveni naziv`) %>% 
  unlist %>% 
  word(start = 1L, end = 2L) %>% 
  str_replace(pattern = 'Linnaeus', replacement = "") %>%
  str_replace(pattern = ',', replacement = "") -> Strogozv$kratki
Strogozv %>% fill(RED, PORODICA, .direction = c("down")) -> Strogozv

#distinct/unique values
eselec %>% inner_join(Strogozv, by = c("merged" = "kratki")) %>% 
  drop_na(merged) %>% 
  distinct(merged, .keep_all=T) -> Strogozv_zahvat

#the end
Strogozv_zahvat %>% write.csv2("strogo_zv_zahvat.csv")
