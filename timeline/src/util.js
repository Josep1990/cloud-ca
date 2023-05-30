import jwt from 'jsonwebtoken';


export function isTokenValid(tokenHeader) {
    if (!tokenHeader) {
        throw new Error('Token header is not present');
    }
    const token = tokenHeader.split(' ')[1]; // Bearer <token>
    if (!token) { 
        throw new Error('Token not present');
    }
    return jwt.verify(token, process.env.JWT_SECRET);
}