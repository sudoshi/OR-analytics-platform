import { Box, Container, Card, CardContent } from "@mui/material";
import { type FC, type ReactNode } from "react";

export const PublicLayout: FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <Container component="main" maxWidth="sm">
      <Box
        sx={{
          height: "100vh",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Card variant="outlined" sx={{ padding: 2 }}>
          <CardContent>{children}</CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default PublicLayout;
