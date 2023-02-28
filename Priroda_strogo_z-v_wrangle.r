library(readxl)
library(dplyr)
library(tidyr)
library(stringr)
library(purr)
Strogozv <- read_excel("//server.intranet.dvokut-ecro.hr/Ecro/2_StrucneUsluge/1_PUOP/2_PUO/OPP_SUO_HV_Retencija_Bregana_Koretici/2_Radno/2_Priroda/GOEM/Nikola G/Popis strogo zasticenih vrsta.xlsx")
Fauna_tablis <- read_excel("//server.intranet.dvokut-ecro.hr/Ecro/2_StrucneUsluge/1_PUOP/2_PUO/OPP_SUO_HV_Retencija_Bregana_Koretici/2_Radno/2_Priroda/GOEM/Nikola G/Fauna-tablis.xlsx")

Fauna_tablis %>% 
  select(Ime_svojte) %>% 
  unlist %>% 
  word(start = 1L, end = 2L) %>% 
  as_tibble() -> Stroge

Strogozv %>% 
  select(`VRSTA - znanstveni naziv`) %>% 
  unlist %>% 
  word(start = 1L, end = 2L) %>% 
  str_replace(pattern = 'Linnaeus', replacement = "") %>%
  str_replace(pattern = ',', replacement = "") -> Strogozv$kratki
Strogozv %>% fill(RED, PORODICA, .direction = c("down")) -> Strogozv

#distinct/unique values
Stroge %>% inner_join(Strogozv, by = c("value" = "kratki")) %>% drop_na(value) %>% unique -> Stroge

Stroge %>% write.csv2("stroge_buraz.csv")
