#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>

std::string DecryptMessage(const std::string& inputFileName, int blocksize)
{
	std::ifstream input(inputFileName);
	std::string encryptedMessage;
	getline(input, encryptedMessage);

	int tableHeight;
	if (encryptedMessage.size() == int(encryptedMessage.size() / blocksize) * blocksize)
		tableHeight = encryptedMessage.size() / blocksize;
	else
	{
		tableHeight = encryptedMessage.size() / blocksize + 1;
		int additionalSpaceAmount = (tableHeight * blocksize) - encryptedMessage.size();
		for (int i = 0; i < additionalSpaceAmount; i++)
			encryptedMessage += " ";
	}

	// writing
	std::vector<std::string> table;
	for (int i = 0; i < blocksize; i++)
	{
		std::string column = encryptedMessage.substr(tableHeight * i, tableHeight);
		if (i == int(i / 2) * 2)
		{
			reverse(column.begin(), column.end());
			table.push_back(column);
		}
		else
			table.push_back(column);
	}

	// reading
	std::string decryptedMessage;
	for (int i = 0; i < table[0].size(); i++)
		for (int o = 0; o < table.size(); o++)
			if (i == int(i / 2) * 2)
				decryptedMessage += table[o][i];
			else
				decryptedMessage += table[(table.size() - 1) - o][i];

	return decryptedMessage;
};

std::string EncryptMessage(const std::string& inputFileName, int blocksize)
{
	std::ifstream input(inputFileName);
	std::string decryptedMessage;
	std::string line;
	while (getline(input, line))
		decryptedMessage += line;

	int tableHeight;
	if (decryptedMessage.size() == int(decryptedMessage.size() / blocksize) * blocksize)
		tableHeight = decryptedMessage.size() / blocksize;
	else
	{
		tableHeight = decryptedMessage.size() / blocksize + 1;
		int additionalSpaceAmount = (tableHeight * blocksize) - decryptedMessage.size();
		for (int i = 0; i < additionalSpaceAmount; i++)
			decryptedMessage += " ";
	}

	// writing
	std::vector<std::string> table;
	for (int i = 0; i < tableHeight; i++)
	{
		std::string string = decryptedMessage.substr(blocksize * i, blocksize);
		if (i == int(i / 2) * 2)
			table.push_back(string);
		else
		{
			reverse(string.begin(), string.end());
			table.push_back(string);
		}
	}

	// reading
	std::string encryptedMessage;
	for (int i = 0; i < table[0].size(); i++)
		for (int o = 0; o < table.size(); o++)
			if (i == int(i / 2) * 2)
				encryptedMessage += table[(table.size() - 1) - o][i];
			else
				encryptedMessage += table[o][i];

	return encryptedMessage;
};

int main(int argc, char* argv[])
{
	if (argc != 5)
	{
		std::cout << "Usage: " << argv[0] << " <mode>(encrypt, decrypt) <blocksize> <input.txt> <output.txt>" << std::endl;
		return 1;
	}

	std::string mode = argv[1];
	int blocksize = std::stoi(argv[2]);
	std::string inputFileName = argv[3];
	std::string outputFileName = argv[4];

	if (mode == "decrypt")
	{
		std::ofstream output(outputFileName);
		output << DecryptMessage(inputFileName, blocksize);
	}
	else if (mode == "encrypt")
	{
		std::ofstream output(outputFileName);
		output << EncryptMessage(inputFileName, blocksize);
	}
	else
		std::cout << "Wrong mode" << std::endl;

	std::cout << "Success" << std::endl;
	return 0;
}