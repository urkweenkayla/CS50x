#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // only accept file name
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // open memory card, error if cannot open
    FILE *input_file = fopen(argv[1], "r");
    if (input_file == NULL)
    {
        printf("Cannot open input file\n");
        return 2;
    }

    // create output file, buffer space for each image, var to store number of images and for file
    // name
    FILE *output_file = NULL;

    uint8_t buffer[512];

    int image_count = 0;

    char output_file_name[8];

    // loop to read data from card until end
    while (fread(buffer, 1, 512, input_file) == 512)
    {
        // check for jpeg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xFF &&
            (buffer[3] >= 0xe0 && buffer[3] <= 0xef))
        {
            // if an image file has been created, close it
            if (output_file != NULL)
            {
                fclose(output_file);
            }

            // name for file, increment image count
            sprintf(output_file_name, "%03d.jpg", image_count++);

            // open output file
            output_file = fopen(output_file_name, "w");

            // error if output file cannot be read
            if (output_file == NULL)
            {
                printf("Cannot open output file");
                return 3;
            }
        }

        // if there is an output file, write image data
        if (output_file != NULL)
        {
            fwrite(buffer, 512, 1, output_file);
        }
    }
    // close output file if there is one
    if (output_file != NULL)
    {
        fclose(output_file);
    }

    // close card file
    fclose(input_file);
    return 0;
}
