#include <stdio.h>
//
//	Jack Nelson, Octiber 2016
//
//	Script that accepts strings from the command line and calculates their
//	information content.
//
int main (int argc, char *argv[]) {
	printf("In main");

	if (argc < 2){
		printf("Usage: %s <word> [alphabet file] \n    Alphabet defaults to English", argv[0]);
	}
	else {
		FILE *alphaFile = NULL;
		// If a third argument is supplied, assume it's an alphabet filename and
		// open and read it in
		if (argc >= 3){
			printf("Reading alphabet from %s", argv[2]);

			FILE *alphaFile = fopen( argv[2], "r");
			if (alphaFile == 0){
				printf("Could not open %s", argv[2]);
			}
		}
		else{
			char defaultAlpha[] = "EnglishAlphabet.txt";
			printf("Reading alphabet from %s", defaultAlpha);

			FILE *alphaFile = fopen(defaultAlpha, "r");
			if (alphaFile == 0){
				printf("Could not open %s", defaultAlpha);
			}
		}

		// Read the alphabet file into a char array
		int x;
		while ( ( x = fgetc(alphaFile)) != EOF){
			printf("%c ", x);
		}
		fclose(alphaFile);
	}
}